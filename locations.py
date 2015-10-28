import pydwimmer
from pydwimmer import utilities
import inspect
import os

class Location(object):

    def __init__(self, file_info, row, col=0, module_path=None):
        self.row = row
        if type(file_info) is list:
            self.path = file_info
        elif type(file_info) is str:
            self.path = path_in_module(file_info)
        else:
            raise ValueError("unknown type of file info")
        self.col = col
        if module_path is None:
            module_path = module_path

    def cursor(self):
        return self.row, self.col

    def filename(self):
        return self.path[-1]

    def filepath(self):
        return "/".join(module_path + self.path) + ".py"

    def python_ref(self):
        return "pydwimmer." + ".".join(self.path)

    def __repr__(self):
        return "Location:({},{})@{}".format(self.row, self.col, self.python_ref())

class SettingDefinition(object):

    def __init__(self, location, setting):
        self.loc = location
        self.setting = setting

    def taken_names(self):
        return [arg.name for arg in self.setting.args]

    def unique_name(self, name):
        taken = self.taken_names()
        s = name
        j = 1
        while s in taken:
            j += 1
            s = "{}{}".format(name, j)
        return s

    def __repr__(self):
        return "SettingDef(loc={}, setting={})".format(self.loc, self.setting)

class SymbolDefinition(object):

    def __init__(self, location, name, args):
        self.loc = location
        self.name = name
        self.args = args

    def render(self):
        return "{}({})".format(self.name, ", ".join(self.args))

    def python_ref(self):
        return "{}.{}".format(self.loc.python_ref(), self.name)

    def __repr__(self):
        return "{}@{}".format(self.render(), self.loc)

def path_in_module(name):
    path = os.path.abspath(os.path.splitext(name)[0]).split("/")
    module_index = utilities.index_in(module_name, path)
    return path[module_index+1:]

def get_location(x):
    return Location(inspect.getsourcefile(x), inspect.getsourcelines(x)[1])

def get_definition(x):
    loc = get_location(x)
    name = x.__name__
    try:
        args = inspect.getargspec(x)[0]
    except TypeError:
        _, args = utilities.remove_bracketed(x.__doc__)
    return SymbolDefinition(loc, name, args)

module_name = __name__.split(".")[0]
module_path = os.path.abspath(os.path.dirname(pydwimmer.__file__)).split("/")
