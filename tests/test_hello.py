from gen.entry_point_gen import EntryPointGenerator
from gen.method_gen import create_method_print_string


def test_hello(tmp_path):
    m_gen = create_method_print_string("run", None, "Hello World!")
    gen = EntryPointGenerator("Hello", m_gen)

    gen.serialize(tmp_path)

    expected_output = """Hello = (
  run = (
    'Hello World!' println
  )

)
"""

    with open(str(tmp_path) + "/Hello.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    assert expected_output == actual_output
