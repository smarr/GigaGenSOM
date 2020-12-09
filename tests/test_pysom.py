from tests.util import assert_runs_to_completion


def test_pysom_can_run_hello_world():
    executed = assert_runs_to_completion(".pysom/core-lib/Examples", "Hello")
    assert executed
