import subprocess


NVME_COMMAND = [
    "sudo",
    "-n",
    "/usr/sbin/nvme",
    "smart-log",
    "/dev/nvme0",
]


def parse_number(value):
    value = value.strip().replace("%", "")

    for part in value.split():
        try:
            return float(part)
        except ValueError:
            continue

    return None


def get_nvme_smart():
    try:
        result = subprocess.run(
            NVME_COMMAND,
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode != 0:
            return None

        data = {}

        for line in result.stdout.splitlines():
            if ":" not in line:
                continue

            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

        return {
            "critical_warning": parse_number(
                data.get("critical_warning", "")
            ),
            "temperature": parse_number(
                data.get("temperature", "")
            ),
            "percentage_used": parse_number(
                data.get("percentage_used", "")
            ),
            "media_errors": parse_number(
                data.get("media_errors", "")
            ),
        }

    except (OSError, subprocess.SubprocessError):
        return None


def get_nvme_health(smart):
    if not smart:
        return "⚪ Unknown"

    if (smart.get("critical_warning") or 0) > 0:
        return "🔴 Critical"

    if (smart.get("media_errors") or 0) > 0:
        return "🔴 Critical"

    if (smart.get("temperature") or 0) >= 70:
        return "⚠️ Warning"

    if (smart.get("percentage_used") or 0) >= 90:
        return "⚠️ Warning"

    return "✅ Healthy"