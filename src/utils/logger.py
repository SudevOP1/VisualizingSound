COLORS = {
    "reset": "\033[39m\033[49m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
}


def log(*, msg: str, func_name: str = "", color: str = "reset") -> None:
    """
    logs a msg with optional color and function name

    args:
        msg: msg to be printed
        func_name: optional function name to prepend
        color: color name (raises ValueError if not valid)

    prints:
        - if func_name is empty:
            <color>msg<reset>

        - if func_name is provided:
            <color>[func_name]<reset> msg
    """

    if color not in COLORS.keys():
        raise ValueError(
            f"color '{color}' not allowed,\navailable colors={list(COLORS.keys())}"
        )

    color = COLORS[color]
    reset = COLORS["reset"]

    if len(func_name) == 0:
        print(f"{color}{msg}{reset}")
    else:
        func_name = f"[{func_name}]"
        print(f"{color}{func_name}{reset} {msg}")
