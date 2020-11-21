from gen.generator import IND
from som.ast.priority import Priority
from som.util import combine_pattern_with_args


class Expression:
    def serialize(
        self, _priority, _self_indent, _nested_indent
    ):  # pylint: disable=no-self-use
        return ""

    def is_newline(self):  # pylint: disable=no-self-use
        return False

    def __str__(self):
        return self.serialize(Priority.STATEMENT, 0, 0)


class Newline(Expression):
    def is_newline(self):
        return True

    def serialize(self, _priority, _self_indent, _nested_indent):
        return "\n"


class Raw(Expression):
    def __init__(self, line):
        # drop new-line and dot at the end
        line = line.strip()
        if line[-1] == ".":
            line = line[:-1]

        self._line = line

    def serialize(self, _priority, self_indent, _nested_indent):
        indent_str = IND * self_indent

        assert isinstance(self._line, str)
        return indent_str + self._line


class Literal(Expression):
    def __init__(self, value):
        assert value is not None
        assert isinstance(value, (int, str))
        self._value = value

    def serialize(self, _priority, self_indent, _nested_indent):
        indent_str = IND * self_indent

        if isinstance(self._value, str):
            return f"'{indent_str}{self._value}'"
        if isinstance(self._value, int):
            return f"{indent_str}{self._value}"

        raise Exception("rest not yet implemented")


class Array(Expression):
    def __init__(self, values):
        self._values = values

    def serialize(self, _priority, self_indent, nested_indent):
        indent_str = IND * self_indent

        result = "#(" + indent_str

        first = True
        for val in self._values:
            if first:
                first = False
            else:
                result += " "
            result += val.serialize(Priority.STATEMENT, 0, nested_indent + 1)

        result += ")"
        return result


class MsgSend(Expression):
    def __init__(self, selector, param_exprs):
        self._selector = selector
        self._param_exprs = param_exprs

    def _msg_kind(self):
        if len(self._param_exprs) == 1:
            return Priority.UNARY
        if len(self._param_exprs) == 2 and ":" not in self._selector[1:]:
            return Priority.BINARY
        return Priority.KEYWORD

    def serialize(self, priority, self_indent, nested_indent):
        indent_str = IND * self_indent

        msg_kind = self._msg_kind()

        expr = self._serialize(indent_str, msg_kind, nested_indent)
        if (
            priority == Priority.STATEMENT
            or (priority == Priority.UNARY and msg_kind == Priority.UNARY)
            or priority > msg_kind
        ):
            return expr
        return "(" + expr + ")"

    def _serialize(self, indent_str, msg_kind, nested_indent):
        if msg_kind == Priority.UNARY:
            rcvr = self._param_exprs[0].serialize(Priority.UNARY, 0, nested_indent)
            return f"{indent_str}{rcvr} {self._selector}"
        if len(self._param_exprs) == 2:
            if msg_kind == Priority.BINARY:
                # this avoids having parentheses around the left hand side expression
                # of a binary message, e.g. to get this result: 1 + 3 - (1 + 3)
                # link: `test_binary_message_sends_to_binary`
                rcvr = self._param_exprs[0].serialize(
                    Priority.KEYWORD, 0, nested_indent
                )
            else:
                rcvr = self._param_exprs[0].serialize(msg_kind, 0, nested_indent)
            arg = self._param_exprs[1].serialize(msg_kind, 0, nested_indent)
            return f"{indent_str}{rcvr} {self._selector} {arg}"
        args = [p.serialize(msg_kind, 0, nested_indent) for p in self._param_exprs[1:]]
        rcvr = f"{self._param_exprs[0].serialize(Priority.KEYWORD, 0, nested_indent)}"
        return f"{indent_str}{rcvr} {combine_pattern_with_args(self._selector, args)}"


class Return(Expression):
    def __init__(self, expr):
        self._expr = expr

    def serialize(self, _priority, self_indent, nested_indent):
        indent_str = IND * self_indent
        return f"{indent_str}^ {self._expr.serialize(Priority.STATEMENT, 0, nested_indent + 2)}"


class Read(Expression):
    def __init__(self, name):
        self._name = name

    def serialize(self, _priority, self_indent, _nested_indent):
        indent_str = IND * self_indent
        return f"{indent_str}{self._name}"


class Write(Expression):
    def __init__(self, name, expr):
        self._name = name
        self._expr = expr

    def serialize(self, _priority, self_indent, nested_indent):
        indent_str = IND * self_indent
        val_expr = self._expr.serialize(Priority.STATEMENT, 0, nested_indent + 2)
        return f"{indent_str}{self._name} := {val_expr}"
