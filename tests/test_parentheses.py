import pytest

from gen.som.ast.basic import Priority, Literal, Read, Return, MsgSend


@pytest.mark.parametrize("priority", list(Priority))
def test_literal(priority):
    lit = Literal(1)

    stmt = lit.serialize(priority, 0, 0)
    assert stmt == "1"


@pytest.mark.parametrize("priority", list(Priority))
def test_read(priority):
    read = Read("self")

    stmt = read.serialize(priority, 0, 0)
    assert stmt == "self"


def test_return_read():
    ret = Return(Read("self"))
    stmt = ret.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "^ self"


def test_return_literal():
    ret = Return(Literal("test"))

    stmt = ret.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "^ 'test'"


def test_return_unary_send():
    ret = Return(MsgSend("print", [Read("self")]))
    stmt = ret.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "^ self print"


def test_return_binary_send():
    ret = Return(MsgSend("+", [Literal(1), Literal(2)]))
    stmt = ret.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "^ 1 + 2"


def test_return_keyword_send():
    ret = Return(MsgSend("max:", [Literal(1), Literal(2)]))
    stmt = ret.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "^ 1 max: 2"


def test_unary_message_sends_with_read():
    expr = MsgSend("print", [Read("self")])
    stmt = expr.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "self print"


def test_unary_message_sends_to_read_to_unary():
    expr = MsgSend("yourself", [Read("self")])
    expr = MsgSend("yourself", [expr])
    stmt = expr.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "self yourself yourself"


def test_unary_message_sends_to_binary():
    binary_msg = MsgSend("+", [Literal(1), Literal(3)])
    expr = MsgSend("print", [binary_msg])

    stmt = expr.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "(1 + 3) print"


def test_binary_message_sends_to_binary():
    binary_msg = MsgSend("+", [Literal(1), Literal(3)])
    expr = MsgSend("-", [binary_msg, binary_msg])

    stmt = expr.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 + 3 - (1 + 3)"


def test_unary_message_sends_to_binary_binary():
    binary_msg = MsgSend("+", [Literal(1), Literal(3)])
    expr = MsgSend("-", [binary_msg, binary_msg])
    expr = MsgSend("print", [expr])

    stmt = expr.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "(1 + 3 - (1 + 3)) print"


def test_binary_message_sends_to_unary():
    rcvr = MsgSend("negated", [Literal(1)])
    binary_msg = MsgSend("+", [rcvr, rcvr])

    stmt = binary_msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 negated + 1 negated"


def test_keyword_to_literals():
    binary_msg = MsgSend("max:", [Literal(1), Literal(1)])

    stmt = binary_msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 max: 1"


def test_keyword_to_binary_msgs():
    rcvr = MsgSend("+", [Literal(1), Literal(1)])
    binary_msg = MsgSend("max:", [rcvr, rcvr])

    stmt = binary_msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 + 1 max: 1 + 1"


def test_keyword_to_unary_msgs():
    rcvr = MsgSend("negated", [Literal(1)])
    binary_msg = MsgSend("max:", [rcvr, rcvr])

    stmt = binary_msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 negated max: 1 negated"


def test_keyword_with_three_parts():
    first = Literal(1)
    second = Literal(10)
    third = Read("self")

    msg = MsgSend("to:do:", [first, second, third])

    stmt = msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 to: 10 do: self"


def test_keyword_with_mixed():
    first = Literal(1)
    second = MsgSend("negated", [Literal(10)])
    third = MsgSend("+", [Literal(5), Literal(55)])

    msg = MsgSend("to:do:", [first, second, third])

    stmt = msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "1 to: 10 negated do: 5 + 55"


def test_unary_to_keyword():
    rcvr = MsgSend("max:", [Literal(1), Literal(1)])
    rcvr = MsgSend("negated", [rcvr])

    stmt = rcvr.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "(1 max: 1) negated"


def test_binary_to_keyword():
    rcvr = MsgSend("max:", [Literal(1), Literal(2)])
    binary_msg = MsgSend("+", [rcvr, Literal(3)])

    stmt = binary_msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "(1 max: 2) + 3"


def test_keyword_to_keyword():
    left = MsgSend("max:", [Literal(0), Literal(1)])
    right = MsgSend("max:", [Literal(2), Literal(3)])

    binary_msg = MsgSend("max:", [left, right])

    stmt = binary_msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "(0 max: 1) max: (2 max: 3)"


def test_regression():
    msg_a = MsgSend("+", [Read("a"), Literal(8)])
    msg_b = MsgSend("/", [Read("b"), msg_a])
    one = MsgSend("-", [Literal(1), msg_b])
    msg = MsgSend("/", [Read("c"), one])

    stmt = msg.serialize(Priority.STATEMENT, 0, 0)
    assert stmt == "c / (1 - (b / (a + 8)))"
