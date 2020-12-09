from gen.som import object_system
from gen.som.ast.basic import MsgSend, Read, Newline
from gen.som.clazz import Class
from gen.som.method import (
    Method,
    set_max_statements_in_method,
    set_desired_statements_in_method,
)


def test_method_helper():
    max_m = 4
    des_m = 3

    set_max_statements_in_method(max_m)
    set_desired_statements_in_method(des_m)

    clazz = Class("Test", object_system.Object, object_system.Empty)
    method = Method("test", clazz)

    for i in range(0, max_m * max_m + 2):
        method.add_statement(MsgSend(f"foobar{i + 1}", [Read("self")]))
        if i % 2 == 0 and i > 0:
            method.add_statement(Newline())

    clazz.add_method(method)

    actual = clazz.serialize_body().strip()
    expect = """test = (
    self helper_test7.
    self helper_test8
  )

  helper_test1 = (
    self foobar1.
    self foobar2.
    self foobar3
  )

  helper_test2 = (
    self foobar4.
    self foobar5.

    self foobar6
  )

  helper_test3 = (
    self foobar7.

    self foobar8.
    self foobar9
  )

  helper_test4 = (
    self foobar10.
    self foobar11.

    self foobar12
  )

  helper_test5 = (
    self foobar13.

    self foobar14.
    self foobar15
  )

  helper_test6 = (
    self foobar16.
    self foobar17.

    self foobar18
  )

  helper_test7 = (
    self helper_test1.
    self helper_test2.
    self helper_test3.
    self helper_test4
  )

  helper_test8 = (
    self helper_test5.
    self helper_test6
  )"""

    print("----------")
    print(actual)
    print("----------")
    assert expect == actual
