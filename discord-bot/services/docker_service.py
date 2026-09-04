import docker


def get_docker_client():
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        return None


def get_docker_health():
    client = get_docker_client()

    if client is None:
        return {
            "available": False,
            "state": "🔴 Critical",
        }

    return {
        "available": True,
        "state": "✅ Healthy",
    }


def get_docker_snapshot():
    client = get_docker_client()

    if client is None:
        return None

    info = client.info()
    containers = client.containers.list(all=True)

    running = 0
    stopped = 0
    container_lines = []

    for container in containers:
        if container.status == "running":
            running += 1
            icon = "🟢"
        else:
            stopped += 1
            icon = "🔴"

        container_lines.append(
            f"{icon} `{container.name}` - `{container.status}`"
        )

    return {
        "version": info.get("ServerVersion", "Unknown"),
        "architecture": info.get("Architecture", "Unknown"),
        "running": running,
        "stopped": stopped,
        "containers": container_lines,
    }