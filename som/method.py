from gen.generator import IND
from som.ast.basic import MsgSend, Read
from som.ast.priority import Priority
from som.util import combine_pattern_with_args

MAX_STATEMENTS_IN_METHOD = 30
_DESIRED_STATEMENTS_IN_METHOD = 20


class Method:
    def __init__(self, method_name, holder_class, arguments=None):
        if arguments is None:
            arguments = []
        self._method_name = method_name
        self._holder_class = holder_class
        self._statements = []
        self._arguments = arguments
        self._locals = []

        self._helpers_split_out = 0

    def get_unused_local(self):
        num_locals = len(self._locals)
        new_local = f"l{(num_locals + 1)}"
        self._locals.append(new_local)
        return new_local

    def get_name(self):
        return self._method_name

    def get_num_arguments(self):
        return len(self._arguments)

    def _split_out_helper_method_if_too_long(self):
        if len(self._statements) < MAX_STATEMENTS_IN_METHOD or len(self._arguments) > 0:
            return

        end = MAX_STATEMENTS_IN_METHOD
        for i in range(len(self._statements) - 1, 1, -1):
            if self._statements[i].is_newline():
                if i > _DESIRED_STATEMENTS_IN_METHOD:
                    end = i
                    break

        split_stmts = self._statements[:end]
        remaining = self._statements[end:]

        self._helpers_split_out += 1
        method = Method(f"helper_{self._method_name}{self._helpers_split_out}", self._holder_class)
        for stmt in split_stmts:
            method.add_statement(stmt)

        self._holder_class.add_method(method)
        self._statements = remaining
        self._statements.insert(0, MsgSend(method.get_name(), [Read("self")]))

    def add_statement(self, expression):
        self._split_out_helper_method_if_too_long()
        self._statements.append(expression)

    def serialize(self, _priority=Priority.STATEMENT, self_indent=1, nested_indent=1):
        indent_str = IND * self_indent
        body = indent_str
        body = self._serialize_method_pattern(body)

        if self._locals:
            body += f"{indent_str}{IND}| "
            for local in self._locals:
                body += f"{local} "
            body += "|\n"

        suppress_terminator = True
        for stmt in self._statements:
            if not suppress_terminator:
                body += ".\n"
            else:
                suppress_terminator = False

            if stmt.is_newline():
                body += "\n"
                suppress_terminator = True
                continue

            body += stmt.serialize(Priority.STATEMENT, nested_indent + 1, nested_indent + 1)

        body = self._serialize_method_closing(body)

        return body

    def _serialize_method_pattern(self, body):
        if len(self._arguments) == 0:
            body += f"{self._method_name} = (\n"
        else:
            assert ":" in self._method_name, "Haven't yet implemented the other cases"
            body += combine_pattern_with_args(self._method_name, self._arguments)
            body += " = (\n"
        return body

    def _serialize_method_closing(self, body):
        return body + f"\n{IND})\n"


class Block(Method):
    def __init__(self, target_class, arguments=None):
        super().__init__("$blockMethod", target_class, arguments)

    def _serialize_method_pattern(self, body):
        body += "["

        for arg in self._arguments:
            body += ":" + arg + " "

        if self._arguments:
            body += "|\n"

        return body

    def _serialize_method_closing(self, body):
        return body + " ]"
