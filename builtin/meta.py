from pydwimmer.compiler import dwim
from pydwimmer.terms import template

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
