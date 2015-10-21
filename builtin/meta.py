import pydwimmer.compiler
import pydwimmer.terms
from pydwimmer.compiler import dwim
from pydwimmer.terms import template
from pydwimmer.builtin.core import answer

@template
class quoted_term:
    "the term with head {} and list of arguments {}"

@template
class setting_template:
    "a setting template with the list of lines {}"

@template
class not_implemented:
    """I don't yet know how to answer the given question"""

@dwim
def meta(template):
    """what action should be taken in the setting with template [template]?"""
    raise not_implemented()

@dwim
def predict(template):
    """try to predict what action should be taken 
    in the setting with template [template],
    without consulting the user
    """
    analogies(template)

@dwim
def analogies(template):
    """what other setting templates are most closely analogous
    to [template], and what are the analogies?
    """
    question(template)

@pydwimmer.compiler.dwim
def question(template):
    """what is the question being answered in the setting with template [template]?"""
    template

