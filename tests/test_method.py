from som import object_system
from som.ast.basic import MsgSend, Read, Newline
from som.clazz import Class
from som.method import Method


def test_method_helper():
    clazz = Class("Test", object_system.Object, object_system.Empty)
    method = Method("test", clazz)

    for i in range(0, 35):
        method.add_statement(MsgSend("foobar", [Read("self")]))
        if i % 8 == 0:
            method.add_statement(Newline())

    clazz.add_method(method)

    actual = clazz.serialize_body().strip()
    expect = """testHelper1 = (
    self foobar.

    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.

    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.

    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar
  )

  test = (
    self testHelper1.

    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.
    self foobar.

    self foobar.
    self foobar
  )"""

    print("----------")
    print(actual)
    print("----------")
    assert expect == actual
