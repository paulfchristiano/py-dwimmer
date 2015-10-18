import terms
from terms import template
import data
import compiler
from compiler import dwim
from_vim = False
try:
    import vim
    from_vim = True
except ImportError:
    pass

transitions = {}
def ask(Q):
    r = Runner(transitions)
    r.ask(Q)
    try:
        return r.run()
    except Aborting:
        pass

class Aborting(Exception):
    pass

def ensure_import(name, buffer):
    for line in buffer:
        split = line.split(" ")
        if split and split[0] == "import":
            for piece in split:
                if piece == name:
                    return 0
    buffer[:0] = ["import {}".format(name)]
    return 1


class Runner(object):
    def __init__(self, transitions):
        self.stack = []
        self.transitions = transitions

    def get_action(self, setting):
        template = setting.head
        if template.id not in self.transitions:
            if from_vim:
                #TODO I should factor out these manipulations into another file probably
                filename, lineno, col = compiler.locations[template.previous().id]
                vim.command("w")
                vim.command("e {}".format(filename))
                template_name, template_file, _ = terms.templates[template.lines()[-1].id]
                if template_file != filename:
                    template_module = ".".join(template_file.split(".")[:-1])
                    lineno += ensure_import(template_module, vim.current.buffer)
                vim.current.buffer[lineno-1:lineno-1] = [
                    "{}with {}:".format( " " * col, 
                        template_name 
                        if template_file == filename 
                        else "{}.{}".format(template_module, template_name)
                    )
                ]
                vim.current.window.cursor = (lineno, col)
                raise Aborting()
            else:
                raise NotImplementedError("can't yet do anything interesting")
                #TODO this needs to deconvert from action type
                #(and of course I need to actually write the meta method)
                action = ask(meta(terms.to_term(setting)))
        return self.transitions[template.id]

    def step(self):
        setting = self.pop()
        if not from_vim:
            print("\n\nstepping in setting:\n{}\n".format("\n".join(str(x) for x in setting.lines())))
        action = self.get_action(setting)
        if not from_vim:
            print("taking action: {}".format(action))
        answer = self.take_action(action, setting)
        if answer is not None:
            if self.stack:
                self.answer(answer)
            else:
                return answer
        return None

    def answer(self, answer):
        self.push(self.pop().append_line(answer))

    def ask(self, question):
        setting = terms.Setting().append_line(question)
        self.push(setting)

    def push(self, setting):
        self.stack.append(setting)

    def pop(self):
        self.stack, result = self.stack[:-1], self.stack[-1]
        return result

    def top(self):
        return self.stack[-1]

    def take_action(self, action, setting):
        setting = setting.append_line(action)
        if action.type == terms.Action.RETURN:
            return action.args[0].instantiate(setting)
        elif action.type == terms.Action.VIEW:
            self.push(setting.append_line(action.args[0].instantiate(setting)))
            return None
        elif action.type == terms.Action.ASK:
            self.push(setting)
            question = action.args[0].instantiate(setting)
            self.ask(question)
            return None
        raise ValueError("action of unknown kind")

    def run(self):
        while True:
            result = self.step()
            if result is not None:
                return result

@template
class not_implemented:
    """I don't yet know how to answer the given question"""

@dwim
def meta(template):
    """what action should be taken in the template [template]?"""
    raise not_implemented()
