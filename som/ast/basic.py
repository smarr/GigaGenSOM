from gen.generator import IND
from som.ast.priority import Priority
from som.method import combine_pattern_with_args


class Expression:
    def serialize(self, _priority, _indent):  # pylint: disable=no-self-use
        return ""

    def __str__(self):
        return self.serialize(Priority.STATEMENT, 0)


class Literal(Expression):
    def __init__(self, value):
        self._value = value

    def serialize(self, _priority, indent):
        indent_str = IND * indent

        if isinstance(self._value, str):
            return f"'{indent_str}{self._value}'"
        if isinstance(self._value, int):
            return f"{indent_str}{self._value}"

        raise Exception("rest not yet implemented")


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

    def serialize(self, priority, indent):
        indent_str = IND * indent

        msg_kind = self._msg_kind()

        expr = self._serialize(indent_str, msg_kind)
        if (
            priority == Priority.STATEMENT
            or (priority == Priority.UNARY and msg_kind == Priority.UNARY)
            or priority > msg_kind
        ):
            return expr
        return "(" + expr + ")"

    def _serialize(self, indent_str, msg_kind):
        if msg_kind == Priority.UNARY:
            rcvr = self._param_exprs[0].serialize(Priority.UNARY, 0)
            return f"{indent_str}{rcvr} {self._selector}"
        if len(self._param_exprs) == 2:
            if msg_kind == Priority.BINARY:
                # this avoids having parentheses around the left hand side expression
                # of a binary message, e.g. to get this result: 1 + 3 - (1 + 3)
                # link: `test_binary_message_sends_to_binary`
                rcvr = self._param_exprs[0].serialize(Priority.KEYWORD, 0)
            else:
                rcvr = self._param_exprs[0].serialize(msg_kind, 0)
            arg = self._param_exprs[1].serialize(msg_kind, 0)
            return f"{indent_str}{rcvr} {self._selector} {arg}"
        args = [p.serialize(msg_kind, 0) for p in self._param_exprs[1:]]
        rcvr = f"{self._param_exprs[0].serialize(Priority.KEYWORD, 0)}"
        return f"{indent_str}{rcvr} {combine_pattern_with_args(self._selector, args)}"


class Return(Expression):
    def __init__(self, expr):
        self._expr = expr

    def serialize(self, _priority, indent):
        indent_str = IND * indent
        return f"{indent_str}^ {self._expr.serialize(Priority.STATEMENT, 0)}"


class Read(Expression):
    def __init__(self, name):
        self._name = name

    def serialize(self, _priority, indent):
        indent_str = IND * indent
        return f"{indent_str}{self._name}"
