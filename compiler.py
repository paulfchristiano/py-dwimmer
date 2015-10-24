import ast
from pydwimmer import terms
from pydwimmer import utilities
from pydwimmer import locations

def debug():
    import ipdb
    ipdb.set_trace()

#maps each setting ID to the location of the last line of code
#defining actions in that setting
setting_definitions = {}

#a queue of arguments to feed to learn_to_code
#these will be executed by learn_from_all once all of the code is read,
#and all of the names have been populated with appropriate stub definitions
to_learn = []

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
            if not hasattr(f, '__doc__'):
                raise ValueError("dwim requires docstring")
            question, newargs = terms.make_template(f.__doc__)
            terms.all_templates.add(question)
            permute = utilities.permutation_from(newargs, args)
            setting = terms.Setting()
            setting.append_line(question(*[terms.RefName(name) for name in newargs]))
            queue_to_learn(fdef.body, setting, f.__globals__, filename, first_line)
            terms.template_definitions[question.id] = locations.get_definition(f)
            def stub(*args):
                import runner
                Q = question(*(args[permute[i]] for i in range(len(args))))
                return runner.ask(Q)
            stub.template = question
            return stub
    else:
        raise ValueError()

def last_line_no(node):
    if hasattr(node, "lineno"):
        last = node.lineno
    else:
        last = -1
    for child in ast.iter_child_nodes(node):
        last = max(last_line_no(child), last)
    return last

def is_call_like(head):
    return isinstance(head, ast.Call) or isinstance(head, ast.BinOp) or isinstance(head, ast.Compare)

def get_answer(setting):
    import builtin
    v = "temp{}".format(len(setting.lines()))
    setting = setting.append_line(builtin.core.answer(terms.RefName(v)))
    return parse_term_constructor(ast.Name(v, ast.Load()), setting, None)

def take_and_save_action(setting, action):
    import runner
    runner.transitions[setting.head.id] = action
    return setting.append_line(action)

def learn_from_code(body, setting, g, filename, first_line, start_line=None, start_col=None):
    import runner, builtin
    try:
        if not body:
            #TODO improve the registering of locations
            #(eliminate redundancy, use a less ambiguous data structure)
            if start_line is None or start_col is None:
                raise ValueError("can't have an empty block")
            setting_definitions[setting.head.id] = locations.SettingDefinition(
                    locations.Location(filename, start_line+first_line-1, start_col),
                    setting
                )
            return
        head = body[0]
        if isinstance(head, ast.Expr):
            value = head.value
            if is_call_like(value):
                Q, setting = parse_term_constructor(value, setting, g, True)
                action = terms.Action.ask(Q)
            elif isinstance(value, ast.Name):
                v, setting = parse_term_constructor(value, setting, g)
                action = terms.Action.view(v)
            elif isinstance(value, ast.Str) or isinstance(value, ast.Pass):
                learn_from_code(body[1:], setting, g, filename, first_line, 
                        last_line_no(value), value.col_offset)
                return
            else:
                raise ValueError("invalid expression type in dwim'd function", value.lineno)
            setting = take_and_save_action(setting, action)
        elif isinstance(head, ast.Return):
            A, setting = parse_term_constructor(head.value, setting, g)
            action = terms.Action.reply(builtin.core.answer(A))
            setting = take_and_save_action(setting, action)
        elif isinstance(head, ast.Raise):
            A, setting = parse_term_constructor(head.type, setting, g)
            action = terms.Action.reply(A)
            setting = take_and_save_action(setting, action)
        elif isinstance(head, ast.If):
            cond = head.test
            #NOTE: this is not top---if it is a question, we should ask then take the answer
            v, setting = parse_term_constructor(cond, setting, g)
            action = terms.Action.view(v)
            setting = take_and_save_action(setting, action)
            learn_from_code(
                head.body, 
                setting.copy().append_line(builtin.bools.yes()), 
                g, filename, first_line
            )
            learn_from_code(
                head.orelse, 
                setting.copy().append_line(builtin.bools.no()), 
                g, filename, first_line
            )
        else:
            raise ValueError("first line of a block was not an expression or return/raise", head.lineno)
        last_line = last_line_no(body[-1])
        setting_definitions[setting.head.id] = locations.SettingDefinition(
                locations.Location(filename, last_line+first_line-1, head.col_offset),
                setting
            )
        for block in body[1:]:
            if isinstance(block, ast.With):
                context = block.context_expr
                if isinstance(context, ast.Call):
                    template = extract_template(context.func, g)
                    arg_names = [terms.RefName(args.id) for args in context.args]
                    new_setting = setting.copy().append_line(template(*arg_names))
                else:
                    raise ValueError("with context is not a function call", context.lineno)
                #TODO here we do the indent manually
                #I don't see how to avoid this, but we can at least be more principled about it
                #rather than assuming that it is 4 spaces...
                learn_from_code(block.body, new_setting, g, filename, first_line, 
                        last_line_no(context), context.col_offset+4)
            else:
                raise ValueError("subsequent line of a block was not a with statement", block.lineno)
    except ValueError, exc:
        if len(exc.args) == 2:
            exc.args = ("{} in line {} of {}".format(exc.args[0], exc.args[1] + first_line - 1, filename),)
        raise

def map_and_fold(xs, y, f):
    """
    apply [f] to each element of [xs] in order.
    use [y] as the second argument of the first invocation,
    and after that use the second output of each invocation
    as the second input into the next one.
    return a pair with the list of first outputs,
    as well as the final second output
    """
    if len(xs) == 0:
        return ([], y)
    else:
        x, y = f(xs[0], y)
        out_list, out_y = map_and_fold(xs[1:], y, f)
        return [x] + out_list, out_y

def parse_term_constructor(value, setting, g, top=False):
    import builtin, runner
    def subparse(value, setting):
        return parse_term_constructor(value, setting, g)
    if isinstance(value, ast.Call):
        func = evaluate(value.func, g)
        new_args, setting = map_and_fold( value.args, setting, subparse)
        if isinstance(func, terms.Template):
            return func(*new_args), setting
        if top:
            if hasattr(func, 'template'):
                return func.template(*new_args), setting
            else:
                raise ValueError("calling function without template", value.lineno)
    if is_call_like(value) and not top:
        Q, setting = parse_term_constructor(value, setting, g, True)
        action = terms.Action.ask(Q)
        setting = take_and_save_action(setting, action)
        v, setting = get_answer(setting)
        return v, setting
    if isinstance(value, ast.List):
        elts, setting = map_and_fold(value.elts, setting, subparse)
        return builtin.lists.to_term(elts), setting
    if isinstance(value, ast.Dict):
        keys, setting = map_and_fold(value.keys, setting, subparse)
        values, setting = map_and_fold(value.values, setting, subparse)
        return builtin.dicts.to_term(dict(zip(values, keys))), setting
    if isinstance(value, ast.Name):
        try:
            return terms.RefNum(utilities.index_in(
                    value.id, [arg.name for arg in setting.args]
                )), setting
        except ValueError, exc:
            exc.args = exc.args + (value.lineno,)
            raise
    if isinstance(value, ast.Num):
        return builtin.ints.to_term(value.n), setting
    if isinstance(value, ast.Str):
        return builtin.strings.to_term(value.s), setting
    #TODO lists and dictionaries
    def from_op(left, op, right, opEquivalents, setting):
        for c in opEquivalents:
            if isinstance(op, c):
                args, setting = map_and_fold([left, right], setting, subparse)
                return opEquivalents[c].template(*args), setting
        raise ValueError("unrecognized operation", value.lineno)
    if isinstance(value, ast.BinOp):
        opEquivalents = {
            ast.Add: builtin.ints.add
        }
        return from_op(value.left, value.op, value.right, opEquivalents, setting)
    if isinstance(value, ast.Compare) and len(value.ops) == 1:
        opEquivalents = {
            ast.Eq: builtin.core.eq
        }
        return from_op(value.left, value.ops[0], value.comparators[0], opEquivalents, setting)
    raise ValueError("unknown type of expression", value.lineno)

def extract_template(value, g):
    concrete = evaluate(value, g)
    if isinstance(concrete, terms.Template):
        return concrete
    elif hasattr(concrete, "template"):
        return concrete.template
    else:
        raise ValueError("extracting template from something without a template", value.lineno)

def evaluate(value, g):
    if isinstance(value, ast.Name):
        name = value.id
        if name in g:
            return g[name]
        elif name in __builtins__:
            return __builtins__[name]
        else:
            raise ValueError("the name {} is not in the global scope".format(name), value.lineno)
    elif isinstance(value, ast.Attribute):
        host = evaluate(value.value, g)
        return getattr(host, value.attr)
    else:
        raise ValueError("unknown type of expression", value.lineno)
