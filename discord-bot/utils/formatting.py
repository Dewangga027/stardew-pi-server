def format_bytes(value: int | float) -> str:
    gb = value / (1024 ** 3)
    return f"{gb:.1f} GB"