from som.ast.basic import MsgSend, Literal
from som.method import Method


def create_method_print_string(method_name, string):
    m = Method(method_name)
    m.add_statement(MsgSend('println', [Literal(string)]))
    return m
