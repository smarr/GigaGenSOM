from gen.generator import IND
from som.ast.priority import Priority


def combine_pattern_with_args(selector, args):
    result = ""
    name_parts = selector.split(":")
    for i in range(0, len(name_parts) - 1):
        if i > 0:
            result += " "
        result += f"{name_parts[i]}: {args[i]}"
    return result


class Method:
    def __init__(self, method_name, arguments=None):
        if arguments is None:
            arguments = []
        self._method_name = method_name
        self._statements = []
        self._arguments = arguments
        self._locals = []

    def get_unused_local(self):
        num_locals = len(self._locals)
        new_local = f"l{(num_locals + 1)}"
        self._locals.append(new_local)
        return new_local

    def get_name(self):
        return self._method_name

    def get_num_arguments(self):
        return len(self._arguments)

    def add_statement(self, expression):
        self._statements.append(expression)

    def serialize(self):
        body = IND
        if len(self._arguments) == 0:
            body += f"{self._method_name} = (\n"
        else:
            assert ":" in self._method_name, "Haven't yet implemented the other cases"
            body += combine_pattern_with_args(self._method_name, self._arguments)
            body += " = (\n"

        if self._locals:
            body += f"{IND}{IND}| "
            for local in self._locals:
                body += f"{local} "
            body += "|\n"

        first = True
        for stmt in self._statements:
            if not first:
                body += ".\n"
            else:
                first = False
            body += stmt.serialize(Priority.STATEMENT, 2)

        body += f"\n{IND})\n"

        return body
