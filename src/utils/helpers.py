import os


def map_num(num: float, x1: float, x2: float, x3: float, x4: float) -> float:
    """linearly maps a numeric value from range [x1, x2] to range [x3, x4]"""
    if x1 == x2:
        return 0
    return x3 + (x4 - x3) * (num - x1) / (x2 - x1)


def resolve_filepath(filepath: str, replace: bool = False) -> str:
    """resolves filename collisions by appending an incrementing numeric suffix"""

    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    base, ext = os.path.splitext(filepath)

    if not os.path.exists(filepath) or replace:
        return filepath

    i = 1
    while True:
        new_filepath = f"{base} ({i}){ext}"
        if not os.path.exists(new_filepath):
            return new_filepath
        i += 1
