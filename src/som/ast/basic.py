from gen.generator import IND
from som.method import combine_pattern_with_args


class Expression(object):
    pass


class Literal(Expression):

    def __init__(self, value):
        self._value = value

    def serialize(self, indent):
        indent_str = IND * indent

        if type(self._value) == str:
            return f"'{indent_str}{self._value}'"
        elif type(self._value) == int:
            return f"{indent_str}{self._value}"

        assert type(self._value) == str, "rest not yet implemented"


class MsgSend(Expression):

    def __init__(self, selector, param_exprs):
        self._selector = selector
        self._param_exprs = param_exprs

    def serialize(self, indent):
        indent_str = IND * indent
        rcvr = f"({self._param_exprs[0].serialize(0)})"

        if len(self._param_exprs) == 1:
            return f"{indent_str}{rcvr} {self._selector}"
        elif len(self._param_exprs) == 2:
            return f"{indent_str}{rcvr} {self._selector} ({self._param_exprs[1].serialize(0)})"
        else:
            args = [p.serialize(0) for p in self._param_exprs[1:]]
            return f"{indent_str}({rcvr} {combine_pattern_with_args(self._selector, args)})"


class Return(Expression):

    def __init__(self, expr):
        self._expr = expr

    def serialize(self, indent):
        indent_str = IND * indent
        return f"{indent_str}^ {self._expr.serialize(0)}"


class Read(Expression):

    def __init__(self, name):
        self._name = name

    def serialize(self, indent):
        indent_str = IND * indent
        return f"{indent_str}{self._name}"
