import platform
from datetime import datetime, timedelta

import psutil


def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    uptime = timedelta(seconds=int(uptime.total_seconds()))

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m"


def get_cpu_temperature():
    thermal_path = "/sys/class/thermal/thermal_zone0/temp"

    try:
        with open(thermal_path, "r", encoding="utf-8") as file:
            raw = float(file.read().strip())
            return raw / 1000
    except (OSError, ValueError):
        return None


def get_throttling():
    try:
        import subprocess

        result = subprocess.run(
            ["vcgencmd", "get_throttled"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip().replace("throttled=", "")

    except (OSError, subprocess.SubprocessError):
        return None


def get_system_snapshot():
    disk_path = "C:\\" if platform.system() == "Windows" else "/"

    return {
        "host": platform.node(),
        "os": platform.system(),
        "architecture": platform.machine(),
        "cpu_usage": psutil.cpu_percent(interval=0.5),
        "memory": psutil.virtual_memory(),
        "disk": psutil.disk_usage(disk_path),
        "uptime": get_uptime(),
        "cpu_temperature": get_cpu_temperature(),
        "throttling": get_throttling(),
    }