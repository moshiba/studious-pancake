"""
pretty prints
"""


def announce(string: str, level: int = 12):
    print("=" * level, end=' ')
    print(string.strip('\n'), end=' ')
    print("=" * level)


def yell(string: str, width: int = 40):
    if len(string) > (width - 8):
        width = len(string) + 8
    print("=" * width)
    i = len(string) % 2
    wing = (width - len(string) - 8) // 2
    print("== " + " " * wing, string.strip('\n'), " " * (wing + i) + " ==")
    print("=" * width)
