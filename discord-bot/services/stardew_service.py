from datetime import datetime, timezone

import docker
from docker.errors import DockerException, NotFound


STARDEW_CONTAINER_NAME = "pi5junimo-server"


def format_uptime(started_at):
    if not started_at:
        return "Unknown"

    try:
        started = datetime.fromisoformat(
            started_at.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)
        delta = now - started

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        if days > 0:
            return f"{days}d {hours}h {minutes}m"

        if hours > 0:
            return f"{hours}h {minutes}m"

        return f"{minutes}m"

    except (ValueError, TypeError):
        return "Unknown"


def format_ports(ports):
    if not ports:
        return "None"

    lines = []

    for container_port, bindings in ports.items():
        if not bindings:
            lines.append(f"{container_port} → internal only")
            continue

        for binding in bindings:
            host_ip = binding.get("HostIp", "0.0.0.0")
            host_port = binding.get("HostPort", "?")

            lines.append(
                f"{host_ip}:{host_port} → {container_port}"
            )

    return "\n".join(lines)


def get_stardew_status():
    default = {
        "exists": False,
        "name": STARDEW_CONTAINER_NAME,
        "status": "not_found",
        "image": "Unknown",
        "uptime": "N/A",
        "ports": "None",
    }

    try:
        client = docker.from_env()
        client.ping()

        try:
            container = client.containers.get(
                STARDEW_CONTAINER_NAME
            )

        except NotFound:
            return default

        container.reload()

        attrs = container.attrs

        state = attrs.get("State", {})
        network = attrs.get("NetworkSettings", {})
        config = attrs.get("Config", {})

        status = state.get(
            "Status",
            container.status,
        )

        started_at = state.get("StartedAt")

        if status == "running":
            uptime = format_uptime(started_at)
        else:
            uptime = "N/A"

        image = config.get("Image", "Unknown")

        ports = format_ports(
            network.get("Ports", {})
        )

        return {
            "exists": True,
            "name": container.name,
            "status": status,
            "image": image,
            "uptime": uptime,
            "ports": ports,
        }

    except DockerException:
        return {
            **default,
            "status": "docker_unavailable",
        }