import intern
import re
from ipdb import set_trace as debug
import utilities

by_type = {}
def register_type(c):
    by_type[c.type_id] = c
    return c


def from_id(id):
    type_id, body = intern.get_all(id, 0, None)
    return by_type[type_id].from_id(body)


class Term(object):
    __slots__ = []


@register_type
class CompoundTerm(Term):
    """
    A term or term constructor defined with the template ID [head] and arguments [args]

    if [_id] is not None, then it is a unique identifier for this term
    """

    type_id = 0

    __slots__ = ["head", "args", "_id"]

    def __init__(self, head, args):
        self.head = head
        self.args = args
        self._id = None
    
    def __repr__(self):
        return str(self.head)

    def line_args(self):
        return self.args

    def line_template(self):
        return self.head

    @property
    def id(self):
        if self._id is None:
            self._id = intern.intern_all(self.type_id, (self.head, self.args))
        return self._id

    @classmethod
    def from_id(cls, id):
        head, args = intern.get_all(id, from_id, [from_id])
        return cls(head, args)

    def to_term(self, quote=True):
        if quote:
            return quoted_term(self.head, self.args)
        return self

    def instantiate(self, context):
        return self.head(*(arg.instantiate(context) for arg in self.args))


@register_type
class Template(object):
    """
    A representation of the term template with list of parts [parts]
    and unique idenfitier [id].
    """

    type_id = 3

    __slots__ = ["parts", "id"]

    def __init__(self, parts):
        if type(parts) is str:
            parts = parts.split("{}")
        self.parts = parts
        self.id = intern.intern_all(self.type_id, parts)

    def __repr__(self):
        return "{}".join(self.parts)

    def __call__(self, *args):
        return CompoundTerm(self, [to_term(arg, quote=False) for arg in args])

    def line_slots(self):
        return len(self.parts)-1

    def line_instantiate(self, *args):
        return self(*args)

    @classmethod
    def from_id(cls, id):
        return Template(intern.get_all(id, [""]))


@register_type
class RefName(Term):
    """
    The term constructor that returns the argument bound to the name [name]
    in the envirormnent where it is instantiated.
    """

    type_id = 1

    __slots__ = ["name"]

    def __init__(self, name):
        self.name = name

    @property
    def id(self):
        return intern.intern_all((self.type_id, self.name))

    @classmethod
    def from_id(cls, id):
        name = intern.get_all(id, "")
        return cls(ndex)


@register_type
class RefNum(Term):
    """
    The term constructor that returns the argument after [index] others
    in the setting where it is instantiated.
    """

    type_id = 1

    __slots__ = ["index"]

    def __init__(self, index):
        self.index = index

    @property
    def id(self):
        return intern.intern_all((self.type_id, self.index))

    def instantiate(self, context):
        return context.args[self.index]

    def __str__(self):
        return "#{}".format(self.index)

    @classmethod
    def from_id(cls, id):
        index = intern.get_all(id, 0)
        return cls(index)


@register_type
class Action(object):
    """
    An action of type [type] with arguments [args] and indices [indices].

    If [_id] is not None, then it is the unique idenfitier of this action.

    The interpretation of each possible type is given in the class definition.
    """

    type_id = 2

    RETURN = 0
    """Return the term obtained by instantiating the first argument."""
    ASK = 1
    """Ask the question obtained by instantiating the first argument."""
    VIEW = 2
    """
    View the term obtained by instantiating the first argument
    (which will typically be a Ref)
    """

    templates = {
        RETURN: "return {}",
        ASK : "ask {}",
        VIEW : "view {}"
    }

    __slots__ = ["type", "args", "indices", "_id"]

    def __init__(self, type, args=[], indices=[]):
        self.type = type
        self.args = args
        self.indices = indices
        self._id = None

    @classmethod
    def reply(cls, t):
        return cls(cls.RETURN, [t])

    @classmethod
    def view(cls, t):
        return cls(cls.VIEW, [t])

    @classmethod
    def ask(cls, t):
        return cls(cls.ASK, [t])

    def __repr__(self):
        return self.templates[self.type].format(*(self.args+self.indices))

    def line_slots(self):
        return 0

    def line_instantiate(self):
        return self

    def line_args(self):
        return []

    def line_template(self):
        return self

    @classmethod
    def from_id(cls, id):
        type, (args, indices) = intern.get_all(id, 0, ([from_id], [0]))
        return cls(type, args, indices)

    @property
    def id(self):
        if self._id is None:
            self._id = intern.intern_all(self.type_id, (self.type,
                                           (self.args, self.indices)))
        return self._id


class SettingTemplate(object):
    """
    A representation of the template for a setting with the unique identifier [id].

    A setting template represents an equivalence class of indistinguishable settings.
    It consists of a sequence of line templates,
    which are either term templates or action templates.
    """

    __slots__ = ["id"]

    def __init__(self, lines=[]):
        if type(lines) is int:
            self.id = lines
        else:
            self.id = intern.intern_list([line.id for line in lines])

    def append_line(self, line):
        """
        Returns a representation of the template formed by appending [line]
        to [self]
        """
        return SettingTemplate(intern.extend_list(self.id, line.id))

    def lines(self):
        return intern.get_all(self.id, [from_id])

    def __str__(self):
        return "\n".join([str(line) for line in self.lines()])

    def to_term(self, quote=True):
        if not quote:
            raise ValueError("can't directly translate Setting")
        return setting_template(to_term(self.lines(), quote=True))

def to_term(x, quote=True):
    import data
    if not quote and isinstance(x, Term):
        return x
    if hasattr(x, 'to_term'):
        return x.to_term(quote)
    elif type(x) is list:
        return data.list_to_term([to_term(y, quote) for y in x])
    elif type(x) is int:
        return data.int_to_term(x)
    elif type(x) is bool:
        return data.bool_to_term(x)
    elif type(x) is str:
        return data.string_to_term(x)
    elif type(x) is dict:
        return data.dict_to_term({to_term(k, quote): to_term(v, quote) for k, v in x.items()})
    elif hasattr(x, '__slots__'):
        args = [(slot, to_term(getattr(x, slot), quote)) for slot in x.__slots__]
        return term_from_args(x.__doc__, args)
    elif hasattr(x, '__dict__'):
        args = [(k, to_term(v, quote)) for k, v in x.__dict__.items()]
        return term_from_args(x.__doc__, args)

def term_from_args(s, args):
    template, keys = make_template(s)
    values = [arg[1] for arg in args]
    input_keys = [arg[0] for arg in args]
    permute = utilities.permutation_from(input_keys, keys)
    return(template(*(values[permute[i]] for i in range(len(keys)))))

def make_template(s):
    s, bracketed = utilities.remove_bracketed(s)
    return Template(s), bracketed

class Setting(object):
    """
    The setting with template represented by [head]
    and list of arguments [args].
    """

    __slots__ = ["head", "args"]

    def __init__(self, lines=[]):
        self.head = SettingTemplate()
        self.args = []
        for line in lines:
            self.append_line(line)

    def append_line(self, line):
        """
        Mutates [self] by appending [line], returns [self].
        """

        self.args.extend(line.line_args())
        self.head = self.head.append_line(line.line_template())
        return self

    def copy(self):
        result = Setting()
        result.head = self.head
        result.args = self.args[:]
        return result

    def lines(self):
        result = []
        to_consume = self.args[:]
        for line_template in self.head.lines():
            args_needed = line_template.line_slots()
            consumed, to_consume = to_consume[:args_needed], to_consume[args_needed:]
            result.append(line_template.line_instantiate(*consumed))
        return result

    def __str__(self):
        return str(self.head)

quoted_term = Template("the term with head {} and list of arguments {}")
setting_template = Template("a setting template with the list of lines {}")
