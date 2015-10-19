from pydwimmer.terms import template

@template
class string:
    """the string with list of characters [chars]"""

def to_term(s):
    return string([char_to_term(c) for c in s])

@template
class char:
    """the character with ASCII code [x]"""

def char_to_term(c):
    return char(ord(c))
