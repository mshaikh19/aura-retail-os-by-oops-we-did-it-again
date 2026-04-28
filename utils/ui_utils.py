import re

def strip_ansi(text):
    """ Removes ANSI escape sequences from a string to get its real length. """
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)

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
