from pydwimmer.terms import template
from pydwimmer.compiler import dwim

@template
class answer:
    """the answer is [A]"""

@template
class probably:
    """the answer is probably [A]"""

#Note: this repeats in other packages
@dwim
def eq(x, y):
    """is [x] equal to [y]?"""
    x
