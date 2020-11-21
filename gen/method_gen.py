from som.ast.basic import MsgSend, Literal
from som.method import Method


def create_method_print_string(method_name, clazz, string):
    method = Method(method_name, clazz)
    method.add_statement(MsgSend("println", [Literal(string)]))
    return method
