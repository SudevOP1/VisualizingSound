COLORS = {
    "reset": "\033[39m\033[49m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
}


def log(*, msg: str, prepend: str = "", color: str = "reset") -> None:
    """
    logs a msg with optional color and function name

    args:
        msg: msg to be printed
        prepend: optional str to prepend
        color: color name (raises ValueError if not valid)

    prints:
        - if prepend is empty:
            <color>msg<reset>

        - if prepend is provided:
            <color>[prepend]<reset> msg
    """

    if color not in COLORS.keys():
        raise ValueError(
            f"color '{color}' not allowed,\navailable colors={list(COLORS.keys())}"
        )

    color = COLORS[color]
    reset = COLORS["reset"]

    if len(prepend) == 0:
        print(f"{color}{msg}{reset}")
    else:
        prepend = f"[{prepend}]"
        print(f"{color}{prepend}{reset} {msg}")
