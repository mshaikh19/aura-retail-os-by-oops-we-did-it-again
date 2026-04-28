import re

from utils.colors import Colors

def strip_ansi(text):
    """ Removes ANSI escape sequences from a string to get its real length. """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def pad_ansi(text, width, align='left'):
    """ Correctly pads a string containing ANSI escape sequences. """
    plain = strip_ansi(text)
    diff = width - len(plain)
    if diff <= 0: return text
    if align == 'left': return text + (' ' * diff)
    if align == 'right': return (' ' * diff) + text
    if align == 'center':
        left = diff // 2
        right = diff - left
        return (' ' * left) + text + (' ' * right)
    return text

def drawBox(title, lines, screen_width=80):
    """ Centralized Box Drawing Engine with Blue theme """
    width = 60
    indent = " " * ((screen_width - width) // 2)
    try:
        # Top Border
        print(f"{indent}{Colors.BLUE}╔{'═'*(width-2)}╗")
        title_plain = strip_ansi(title)
        title_pad = pad_ansi(title_plain, width-4, 'center')
        print(f"{indent}{Colors.BLUE}║ {Colors.TEXT}{Colors.BOLD}{title_pad}{Colors.BLUE} ║")
        print(f"{indent}{Colors.BLUE}╠{'═'*(width-2)}╣")
        for line in lines:
            line_plain = strip_ansi(line)
            diff = (width - 4) - len(line_plain)
            padding = " " * max(0, diff)
            # Content in White (TEXT) for a clean blue-themed console
            print(f"{indent}{Colors.BLUE}║ {Colors.TEXT}{line}{Colors.RESET}{padding}{Colors.BLUE} ║")
        print(f"{indent}{Colors.BLUE}╚{'═'*(width-2)}╝{Colors.RESET}")
    except UnicodeEncodeError:
        print(indent + Colors.BLUE + "+" + "-"*(width-2) + "+")
        print(indent + Colors.BLUE + "| " + Colors.TEXT + title.center(width-4) + Colors.BLUE + " |")
        print(indent + Colors.BLUE + "+" + "-"*(width-2) + "+")
        for line in lines:
            print(indent + Colors.BLUE + "| " + Colors.TEXT + line.ljust(width-4) + Colors.BLUE + " |")
        print(indent + Colors.BLUE + "+" + "-"*(width-2) + "+" + Colors.RESET)
