from gen.generator import IND


class Expression(object):
    pass


class Literal(Expression):

    def __init__(self, value):
        self._value = value

    def serialize(self, indent):
        indent_str = IND * indent

        assert type(self._value) == str, "rest not yet implemented"
        return f"'{indent_str}{self._value}'"


class MsgSend(Expression):

    def __init__(self, selector, param_exprs):
        self._selector = selector
        self._param_exprs = param_exprs

    def serialize(self, indent):
        indent_str = IND * indent

        assert len(self._param_exprs) == 1, "rest not implemented"

        return f"{indent_str}({self._param_exprs[0].serialize(0)}) {self._selector}"

