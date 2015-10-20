class Interner(object):
    __slots__ = ['ids', 'keys']

    def __init__(self):
        self.ids = {}
        self.keys = []

    def intern(self, k):
        if k in self.ids:
            return self.ids[k]
        id = len(self.keys)
        self.keys.append(k)
        self.ids[k] = id
        return id

    def get(self, k):
        return self.keys[k]


string_interner = Interner()
def intern_string(s):
    return string_interner.intern(s)
def get_string(id):
    return string_interner.get(id)


int_interner = Interner()
def intern_int(n):
    return int_interner.intern(n)
def get_int(id):
    return int_interner.get(id)


pair_interner = Interner()
def intern_pair(a, b=None):
    if b is not None:
        a = (a, b)
    assert type(a) is tuple
    return pair_interner.intern(a)
def get_pair(id):
    return pair_interner.get(id)


def intern_list(s):
    if len(s) == 0:
        return -1
    prefix = intern_list(s[:-1])
    return intern_pair(prefix, s[-1])


def get_list(id):
    result = []
    while id != -1:
        id, last = get_pair(id)
        result.append(last)
    return list(reversed(result))

extend_list = intern_pair
init_and_last = get_pair


def get_all(id, kind, *args):
    if len(args) == 1:
        kind = (kind, args[0])
    if type(kind) == type(None):
        return id
    if type(kind) == int:
        return get_int(id)
    if type(kind) == str:
        return get_string(id)
    if type(kind) == tuple:
        return tuple([get_all(x, t) for x, t in zip(get_pair(id), kind)])
    if type(kind) == list:
        return [get_all(x, kind[0]) for x in get_list(id)]
    if type(id) == type:
        raise ValueError("get_all takes prototypes, not types")
    else:
        return kind(id)


def intern_all(x, *args):
    if len(args) == 1:
        x = (x, args[0])
    if type(x) is int:
        return intern_int(x)
    if type(x) is str:
        return intern_string(x)
    if type(x) is list:
        return intern_list([intern_all(y) for y in x])
    if type(x) is tuple and len(x) == 2:
        return intern_pair(*[intern_all(y) for y in x])
    if hasattr(x, 'id'):
        return x.id
    raise ValueError("interning unknown type of object")
