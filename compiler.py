import ast
import terms
from ipdb import set_trace as debug
import utilities
import runner
import data

#maps each setting ID to the location of the last line of code
#defining actions in that setting
locations = {}

to_learn = []

def testing():
    print("loaded pydwimmer")

def queue_to_learn(*args):
    to_learn.append(args)

def learn_from_all():
    for args in to_learn:
        learn_from_code(*args)

def dwim(f):
    source, filename, first_line = utilities.uncompile(f.func_code)
    tree = ast.parse(source)
    if isinstance(tree, ast.Module):
        fdef = tree.body[0]
        if isinstance(fdef, ast.FunctionDef):
            args = [x.id for x in fdef.args.args]
            if getattr(f, '__doc__', None) is None:
                raise ValueError("dwim requires docstring")
            question, newargs = terms.make_template(f.__doc__)
            permute = utilities.permutation_from(newargs, args)
            setting = terms.Setting()
            setting.append_line(question(*[terms.RefName(name) for name in newargs]))
            queue_to_learn(fdef.body, setting, f.__globals__, filename, first_line)
            def stub(*args):
                Q = question(*(args[permute[i]] for i in range(len(args))))
                return runner.ask(Q)
            stub.template = question
            return stub
    else:
        raise ValueError()

def last_line_of(node):
    if hasattr(node, "lineno"):
        last = node.lineno
    else:
        last = -1
    for child in ast.iter_child_nodes(node):
        last = max(last_line_of(child), last)
    return last

def is_call_like(head):
    return isinstance(head, ast.Call) or isinstance(head, ast.BinOp) or isinstance(head, ast.Compare)

def learn_from_code(body, setting, g, filename, first_line):
    def register_action(action):
        runner.transitions[setting.head.id] = action
    head = body[0]
    if isinstance(head, ast.Expr):
        value = head.value
        if is_call_like(value):
            Q = parse_term_constructor(value, setting, g, True)
            action = terms.Action.ask(Q)
        elif isinstance(value, ast.Name):
            v = parse_term_constructor(value, setting, g)
            action = terms.Action.view(v)
        elif isinstance(value, ast.Str):
            return learn_from_code(body[1:], setting, g, filename, first_line)
        else:
            raise ValueError("invalid expression type in dwim'd function")
    elif isinstance(head, ast.Return):
        A = parse_term_constructor(head.value, setting, g)
        action = terms.Action.reply(data.answer(A))
    elif isinstance(head, ast.Raise):
        A = parse_term_constructor(head.type, setting, g)
        action = terms.Action.reply(A)
    else:
        raise ValueError("first line of a block was not an expression or return/raise")
    register_action(action)
    setting = setting.append_line(action)
    last_line = last_line_of(body[-1])
    locations[setting.head.id] = (filename, last_line+first_line, head.col_offset)
    for block in body[1:]:
        if isinstance(block, ast.With):
            context = block.context_expr
            if isinstance(context, ast.Call):
                template = extract_template(context.func, g)
                arg_names = [terms.RefName(args.id) for args in context.args]
                new_setting = setting.copy().append_line(template(*arg_names))
            else:
                raise ValueError("with context is not a function call")
            learn_from_code(block.body, new_setting, g, filename, first_line)
        else:
            raise ValueError("subsequent line of a block was not a with statement")

def temp_var(setting):
    return "temp{}".format(len(setting.lines()))

def parse_term_constructor(value, setting, g, top=False):
    import builtins
    if isinstance(value, ast.Call):
        func = eval(value.func.id, g)
        args = [parse_term_constructor(x, setting, g) for x in value.args]
        if isinstance(func, terms.Template):
            return func(*args)
        if top:
            if hasattr(func, 'template'):
                return func.template(*args)
            else:
                raise ValueError("calling function without template")
    if is_call_like(value) and not top:
        #NOTE I just literally edit the setting if I encounter an intermediate value
        #this is pretty unsavory! but it happens to work
        #(it also relies on mutability of settings)
        Q = parse_term_constructor(value, setting, g, True)
        action = terms.Action.ask(Q)
        runner.transitions[setting.head.id] = action
        setting.append_line(action)
        v = temp_var(setting)
        setting.append_line(data.answer(terms.RefName(v)))
        return parse_term_constructor(ast.Name(v, ast.Load()), setting, g)
    if isinstance(value, ast.List):
        return terms.list_to_term([parse_term_constructor(x, setting, g) for x in value.elts])
    if isinstance(value, ast.Dict):
        return terms.dict_to_term({
            parse_term_constructor(k, setting, g):parse_term_constructor(v, setting, g)
            for k, v in zip(value.keys, value.values)
        })
    if isinstance(value, ast.Name):
        for i, s in enumerate(setting.args):
            if value.id == s.name:
                return terms.RefNum(i)
        else:
            raise ValueError("name does not appear in setting")
    if isinstance(value, ast.Num):
        return data.int_to_term(value.n)
    if isinstance(value, ast.Str):
        return data.string_to_term(value.s)
    #TODO lists and dictionaries
    def from_op(left, op, right, opEquivalents):
        for c in opEquivalents:
            if isinstance(op, c):
                return opEquivalents[c].template(
                    parse_term_constructor(left, setting, g),
                    parse_term_constructor(right, setting, g)
                )
        raise ValueError("unrecognized operation")
    if isinstance(value, ast.BinOp):
        opEquivalents = {
            ast.Add: builtins.add
        }
        return from_op(value.left, value.op, value.right, opEquivalents)
    if isinstance(value, ast.Compare) and len(value.ops) == 1:
        opEquivalents = {
            ast.Eq: builtins.eq
        }
        return from_op(value.left, value.ops[0], value.comparators[0], opEquivalents)
    raise ValueError("unknown type of expression")

def extract_template(value, g):
    concrete = eval(value.id, g)
    if isinstance(concrete, terms.Template):
        return concrete
    elif hasattr(concrete, "template"):
        return concrete.template
    else:
        raise ValueError("extracting template from something without a template")
