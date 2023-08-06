from typing import Final


MAPPING: Final = {
    "ᛙ": "f",
    "╮": "u",
    "ו": "þ",
    "ˎ": "o",
    "◟": "r",
    "ᛍ": "k",
    "ᚽ": "h",
    "⸜": "n",
    "ᛁ": "i",
    "⸝": "a",
    "╵": "s",
    "⸍": "t",
    "ˏ": "b",
    "⠃": "m",
    "⸌": "l",
    "⡄": "R",
    ":": " ",
}


def get_rune_mapping() -> dict[str, str]:
    return MAPPING
