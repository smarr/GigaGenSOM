from gen.generator import IND


class Method(object):

    def __init__(self, method_name, arguments = None):
        if arguments is None:
            arguments = []
        self._method_name = method_name
        self._statements = []
        self._arguments = arguments

    def add_statement(self, expression):
        self._statements.append(expression)

    def serialize(self):
        assert len(self._arguments) == 0, "Haven't yet implemented the other cases"

        body = f"{IND}{self._method_name} = (\n"

        first = True
        for stmt in self._statements:
            if not first:
                body += ".\n"
            else:
                first = False
            body += stmt.serialize(2)

        body += f"\n{IND})\n"

        return body

