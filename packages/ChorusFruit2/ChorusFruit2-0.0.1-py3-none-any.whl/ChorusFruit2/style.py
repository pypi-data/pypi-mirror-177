"""Style Functions and Variables"""
fore = {'BLACK': '\x1b[30m', 'BLUE': '\x1b[34m', 'CYAN': '\x1b[36m',
        'GREEN': '\x1b[32m', 'GRAY': '\x1b[90m', 'LIGHTBLUE': '\x1b[94m',
        'LIGHTCYAN': '\x1b[96m', 'LIGHTGREEN': '\x1b[92m',
        'LIGHTMAGENTA': '\x1b[95m', 'LIGHTRED': '\x1b[91m',
        'LIGHTWHITE': '\x1b[97m', 'LIGHTYELLOW': '\x1b[93m',
        'MAGENTA': '\x1b[35m', 'RED': '\x1b[31m', 'RESET': '\x1b[39m',
        'WHITE': '\x1b[37m', 'YELLOW': '\x1b[33m'}
back = {'B_BLACK': '\x1b[40m', 'B_BLUE': '\x1b[44m', 'B_CYAN': '\x1b[46m',
        'B_GREEN': '\x1b[42m', 'B_GRAY': '\x1b[100m',
        'B_LIGHTBLUE': '\x1b[104m', 'B_LIGHTCYAN': '\x1b[106m',
        'B_LIGHTGREEN': '\x1b[102m', 'B_LIGHTMAGENTA': '\x1b[105m',
        'B_LIGHTRED': '\x1b[101m', 'B_LIGHTWHITE': '\x1b[107m',
        'B_LIGHTYELLOW': '\x1b[103m', 'B_MAGENTA': '\x1b[45m',
        'B_RED': '\x1b[41m', 'B_RESET': '\x1b[49m', 'B_WHITE': '\x1b[47m',
        'B_YELLOW': '\x1b[43m'}
other = {'BRIGHT': '\x1b[1m', 'DIM': '\x1b[2m', 'NORMAL': '\x1b[22m',
         'RESET_ALL': '\x1b[0m', 'BOLD': '\x1b[1m', 'UNDERLINE': '\x1b[4m',
         'ITALIC': '\x1b[3m', 'BLINK': '\x1b[5m', 'REVERSE': '\x1b[7m',
         'INVISIBLE': '\x1b[8m', 'STRIKETHROUGH': '\x1b[9m'}
styles = fore | back | other
styles_SquareBrackets = {f'[{k}]': v
                         for (k, v) in zip(styles.keys(), styles.values())}


def apply_style(text: str) -> str:
    """
    Colorize a Text
        Args:
            text[str]: Changes Color IDs with Colors
    """
    for i in styles_SquareBrackets:
        text = text.replace(i, styles_SquareBrackets[i])
    return text + styles['RESET_ALL']


def apply_style_noreset(text: str) -> str:
    """
    Colorize a Text
        Args:
            text[str]: Changes Color IDs with Colors
    """
    for i in styles_SquareBrackets:
        text = text.replace(i, styles_SquareBrackets[i])
    return text


def color_text_with_rgb(text: str, color: tuple, _type: str = 'f') -> str:
    """
    add color to a text with RGB Values
        Args:
            text[str]: Text to color
            color[tuple(R, G, B)]: RGB Values
    """
    red = color[0]
    green = color[1]
    blue = color[2]
    if _type == 'f':
        return f"\x1b[38;2;{red};{green};{blue}m" + text + styles['RESET_ALL']
    elif _type == 'b':
        return f"\x1b[48;2;{red};{green};{blue}m" + text + styles['RESET_ALL']
    else:
        raise TypeError
