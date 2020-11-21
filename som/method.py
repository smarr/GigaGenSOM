from gen.generator import IND
from som.ast.basic import MsgSend, Read
from som.ast.priority import Priority
from som.util import combine_pattern_with_args

_max_statements_in_method: int = 30
_desired_statements_in_method: int = 20


def get_max_statements_in_method():
    return _max_statements_in_method


def set_max_statements_in_method(val):
    global _max_statements_in_method  # pylint: disable=global-statement,invalid-name
    _max_statements_in_method = val


def get_desired_statements_in_method():
    return _desired_statements_in_method


def set_desired_statements_in_method(val):
    global _desired_statements_in_method  # pylint: disable=global-statement,invalid-name
    _desired_statements_in_method = val


class Method:
    def __init__(self, method_name, holder_class, arguments=None):
        if arguments is None:
            arguments = []
        self._method_name = method_name
        self._holder_class = holder_class
        self._statements = []
        self._arguments = arguments
        self._locals = []

        self._helper_methods = []

    def get_unused_local(self):
        num_locals = len(self._locals)
        new_local = f"l{(num_locals + 1)}"
        self._locals.append(new_local)
        return new_local

    def get_name(self):
        return self._method_name

    def get_num_arguments(self):
        return len(self._arguments)

    def _turn_into_helpers(self, statements):
        new_helpers = []
        while statements:
            # remove empty lines at the top
            while statements and statements[0].is_newline():
                statements.pop(0)

            if not statements:
                break

            end = self._find_logic_break(statements)

            split_stmts = statements[:end]
            remaining = statements[end:]

            helper = Method(
                f"helper_{self._method_name}{len(self._helper_methods) + 1}",
                self._holder_class,
            )
            for stmt in split_stmts:
                helper.add_statement(stmt)

            self._helper_methods.append(helper)
            new_helpers.append(helper)

            self._holder_class.add_method(helper)
            statements = remaining

        return new_helpers

    @staticmethod
    def _find_logic_break(statements):
        # use new lines as logical dividers, and try to find one close to the max size for methods
        end = min(len(statements), _max_statements_in_method)
        for i in range(end - 1, 1, -1):
            if statements[i].is_newline():
                if i > _desired_statements_in_method:
                    end = i
                    break
        return end

    def add_statement(self, expression):
        self._statements.append(expression)

    def _split_into_helpers_if_needed(self):
        if (
            len(self._statements) <= _max_statements_in_method
            or len(self._arguments) > 0
        ):
            return False

        helpers = self._turn_into_helpers(self._statements)
        self._statements = [
            MsgSend(helper.get_name(), [Read("self")]) for helper in helpers
        ]
        return True

    def serialize(self, _priority=Priority.STATEMENT, self_indent=1, nested_indent=1):
        while self._split_into_helpers_if_needed():
            pass

        indent_str = IND * self_indent
        body = indent_str
        body = self._serialize_method_pattern(body)

        if self._locals:
            body += f"{indent_str}{IND}| "
            for local in self._locals:
                body += f"{local} "
            body += "|\n"

        # remove empty lines at start and end
        while self._statements[0].is_newline():
            self._statements.pop(0)
        while self._statements[-1].is_newline():
            self._statements.pop()

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

            body += stmt.serialize(
                Priority.STATEMENT, nested_indent + 1, nested_indent + 1
            )

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

    def _serialize_method_closing(self, body):  # pylint: disable=no-self-use
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
