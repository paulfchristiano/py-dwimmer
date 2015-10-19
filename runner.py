import pydwimmer.terms as terms
from pydwimmer.terms import template
import pydwimmer.compiler as compiler
from pydwimmer.compiler import dwim
import pydwimmer.builtin as builtin
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
                filename, lineno, col, taken_names = compiler.locations[template.previous().id]
                vim.command("w")
                vim.command("e {}".format(filename))
                template_name, template_path, arg_names, _ = terms.templates[template.lines()[-1].id]
                for i in range(len(arg_names)):
                    arg = arg_names[i]
                    if arg in taken_names:
                        j = 2
                        while arg in taken_names:
                            arg = arg_names[i] + str(j)
                            j+=1
                    arg_names[i] = arg
                #TODO I should make the file processing less terrifying
                template_file = template_path.split(".")[-1]
                if template_file != filename:
                    lineno += ensure_import(template_path, vim.current.buffer)
                vim.current.buffer[lineno:lineno] = [
                    "{}with {}({}):".format( " " * col, 
                        template_name 
                        if template_file == filename 
                        else "{}.{}".format(template_path, template_name),
                        ", ".join(arg_names)
                    )
                ]
                vim.current.window.cursor = (lineno+1, col)
                raise Aborting()
            else:
                raise NotImplementedError("can't yet do anything interesting")
                #TODO this needs to deconvert from action type
                #(and of course I need to actually write the meta method)
                action = ask(builtin.meta.what_to_do(terms.to_term(setting)))
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
