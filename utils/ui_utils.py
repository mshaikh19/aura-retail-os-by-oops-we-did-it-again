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


def render_table(headers, rows, title=None, screen_width=80, alignments=None):
    """Render a boxed table with Unicode borders. Handles ANSI colors safely.

    headers: list of header strings
    rows: list of row lists (strings)
    """
    # compute column widths based on stripped lengths
    cols = len(headers)
    col_max = [len(strip_ansi(h)) for h in headers]
    for r in rows:
        for i in range(cols):
            cell = r[i] if i < len(r) else ""
            col_max[i] = max(col_max[i], len(strip_ansi(str(cell))))

    # add padding of 2 (one space each side)
    inner = [w + 2 for w in col_max]
    alignments = alignments or ['left'] * cols
    if len(alignments) < cols:
        alignments = alignments + ['left'] * (cols - len(alignments))

    table_width = sum(inner) + (cols - 1)  # account for column separators
    indent = " " * max(0, (screen_width - table_width - 2) // 2)

    try:
        # top border
        top = indent + Colors.BLUE + "╔" + "╦".join(["═" * w for w in inner]) + "╗"
        print(top)

        # title row if provided
        if title:
            title_plain = strip_ansi(title)
            title_pad = pad_ansi(title, table_width, 'center')
            print(f"{indent}{Colors.BLUE}║{Colors.RESET}{title_pad}{Colors.BLUE}║")
            print(indent + Colors.BLUE + "╠" + "╬".join(["═" * w for w in inner]) + "╣")

        # header
        header_cells = [pad_ansi(f" {h} ", inner[i], 'center') for i, h in enumerate(headers)]
        print(indent + Colors.BLUE + "║" + Colors.RESET + "║".join(header_cells) + Colors.BLUE + "║")

        # separator
        print(indent + Colors.BLUE + "╠" + "╬".join(["═" * w for w in inner]) + "╣")

        # rows
        for ri, r in enumerate(rows):
            cells = []
            for i in range(cols):
                cell = str(r[i]) if i < len(r) else ""
                cells.append(pad_ansi(f" {cell} ", inner[i], alignments[i]))
            print(indent + Colors.BLUE + "║" + Colors.RESET + "║".join(cells) + Colors.BLUE + "║")

        # bottom border
        print(indent + Colors.BLUE + "╚" + "╩".join(["═" * w for w in inner]) + "╝" + Colors.RESET)
    except UnicodeEncodeError:
        # fallback simple ascii
        width = sum(inner) + cols - 1
        print(indent + "+" + "-" * width + "+")
        if title:
            print(indent + "| " + title.center(width-2) + " |")
            print(indent + "+" + "-" * width + "+")
        header_line = "|" + "|".join([h.center(inner[i]) for i, h in enumerate(headers)]) + "|"
        print(indent + header_line)
        print(indent + "+" + "-" * width + "+")
        for r in rows:
            row_line = "|" + "|".join([str(r[i]).ljust(inner[i]) if i < len(r) else "" .ljust(inner[i]) for i in range(cols)]) + "|"
            print(indent + row_line)
        print(indent + "+" + "-" * width + "+")
