def convert_milliseconds(milliseconds: float) -> str:
    """Format a duration given in milliseconds as ``"Xd Yh Zm Ws Vms"``."""
    seconds = milliseconds // 1000
    r_ms = milliseconds % 1000
    minutes = seconds // 60
    r_s = seconds % 60
    hours = minutes // 60
    r_m = minutes % 60
    days = hours // 24
    r_h = hours % 24

    parts: list[str] = []
    if days:
        parts.append(f"{int(days)}d")
    if r_h:
        parts.append(f"{int(r_h)}h")
    if r_m:
        parts.append(f"{int(r_m)}m")
    if r_s:
        parts.append(f"{int(r_s)}s")
    if r_ms:
        parts.append(f"{r_ms}ms")
    return " ".join(parts)
