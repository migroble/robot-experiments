from robot.result import ResultVisitor
from robot.result.model import Body


class MessageCollector(ResultVisitor):
    def __init__(self):
        self.msgs = Body()
        self.assign = ()

    def start_keyword(self, kw):
        self.assign = kw.assign

    def end_keyword(self, _kw):
        self.assign = ()

    def start_message(self, msg):
        for v in self.assign:
            if msg.message.startswith("{} = ".format(v)):
                vars = list(self.assign)
                vars.remove(v)
                self.assign = tuple(vars)
                return

        self.msgs.append(msg)


class LogScrubber(ResultVisitor):
    def process_children(self, parent):
        new_body = Body()
        for child in parent.body:
            if (
                child.type == "KEYWORD"
                and child.status != "NOT RUN"
                and ("inline" in child.tags or child.name == "BuiltIn.Run Keyword")
            ):
                self.visit_keyword(child)
                new_body.extend(child.body)
                if child.has_teardown:
                    new_body.append(child.teardown)
            else:
                new_body.append(child)
        parent.body = new_body

    def start_keyword(self, kw):
        if "opaque" in kw.tags:
            c = MessageCollector()
            kw.body.visit(c)
            kw.body = c.msgs
        elif "unroll" in kw.tags:
            new_body = Body()
            for child in kw.body:
                if child.type in ("FOR", "WHILE"):
                    new_body.extend(child.body)

                    # Comment the previous line and uncomment the following lines
                    # to not include the "ITERATION" nodes

                    # for iter in child.body:
                      # new_body.extend(iter.body)
                else:
                    new_body.append(child)
            kw.body = new_body

        self.process_children(kw)

    def start_test(self, test):
        self.process_children(test)

    def start_if_branch(self, branch):
        self.process_children(branch)

    def start_try_branch(self, branch):
        self.process_children(branch)

    def start_for_iteration(self, iter):
        self.process_children(iter)

    def start_while_iteration(self, iter):
        self.process_children(iter)
