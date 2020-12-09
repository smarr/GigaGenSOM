from gen.entry_point_gen import EntryPointGenerator
from gen.method_gen import create_method_print_string
from tests.util import read_file, assert_runs_to_completion


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

    actual_output = read_file(tmp_path, "Hello.som")
    assert expected_output == actual_output
    assert_runs_to_completion(tmp_path, "Hello")
