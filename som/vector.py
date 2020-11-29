from som.ast.basic import Array, Read, Literal, MsgSend, Write, Return
from som.method import Method, get_max_statements_in_method

_MAX_LITERALS = 50


def contains_only_numbers(values):
    for value in values:
        if not str(value)[0].isnumeric():
            return False
    return True


def create_vector_or_array(values, target_class, factory_name):
    if len(values) <= _MAX_LITERALS and contains_only_numbers(values):
        return Array(values)

    if target_class.has_method(factory_name):
        return MsgSend(factory_name, [Read("self")])

    # Otherwise we create a factory method for a Vector
    factory_m = Method(factory_name, target_class)
    target_class.add_method(factory_m)
    new_vector = MsgSend("new:", [Read("Vector"), Literal(len(values))])

    vector = factory_m.get_unused_local()
    write = Write(vector, new_vector)
    factory_m.add_statement(write)

    remaining_values = values[:]
    i = 1
    stmt_cnt = 0

    helper_m = _new_helper(factory_m, factory_name, i, target_class, vector)
    while remaining_values:
        val = remaining_values.pop(0)
        helper_m.add_statement(MsgSend("append:", [Read("vector"), val]))
        stmt_cnt += 1

        if stmt_cnt == get_max_statements_in_method() and remaining_values:
            i += 1
            helper_m = _new_helper(factory_m, factory_name, i, target_class, vector)
            stmt_cnt = 0

    factory_m.add_statement(Return(Read(vector)))

    return MsgSend(factory_name, [Read("self")])


def _new_helper(factory_m, factory_name, i, target_class, vector):
    helper_name = f"{factory_name}Part{i}:"
    factory_m.add_statement(MsgSend(helper_name, [Read("self"), Read(vector)]))
    helper_m = Method(helper_name, target_class, ["vector"])
    target_class.add_method(helper_m)
    return helper_m
