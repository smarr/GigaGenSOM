def read_file(path, file_name):
    with open(str(path) + f"/{file_name}", "r") as output_file:
        return "".join(output_file.readlines())


def assert_runs_to_completion(tmp_path, class_name):
    try:
        from som.vm.universe import (  # pylint: disable=import-outside-toplevel
            create_universe,
            set_current,
        )
    except ImportError:
        return False

    args = ["-cp", ".pysom/core-lib/Smalltalk:" + str(tmp_path), class_name]
    uni = create_universe(True)
    set_current(uni)
    uni.interpret(args)

    assert uni.last_exit_code() == 0
    return True
