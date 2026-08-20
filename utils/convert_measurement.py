def convert_measurement(output: str) -> list[int]:
    """Convert a space-separated bit-string measurement into a list of ints."""
    return [int(part, 2) for part in output.split(" ")]
