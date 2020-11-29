import re
from random import Random
from typing import List, Optional

from gen.spec_types import SPEC_PART_MARKER, SPEC_FULL_MARKER
from som import object_system
from som.ast.basic import Raw, Newline, MsgSend, Write, Read, Return
from som.clazz import Class
from som.method import Method, Block
from som.vector import create_vector_or_array

_DEFAULT_VAL_SETS = {
    "oneOfEachBasicType": [
        "true",
        "false",
        "#foo",
        "123",
        "0.123",
        "'string'",
        "#(1 2)",
        "[ 42 ]",
        "nil",
        "Object new",
    ],
    "allIntVals": [
        "0",
        "-0",
        "1",
        "-1",
        "2147483647",
        "2147483648",  # 31-bit
        "4294967295",
        "4294967296",  # 32-bit
        "9223372036854775807",
        "9223372036854775808",  # 63-bit
        "18446744073709551615",
        "18446744073709551616",  # 64-bit
        "170141183460469231731687303715884105727",
        "170141183460469231731687303715884105728",  # 127-bit
        "340282366920938463463374607431768211455",
        "340282366920938463463374607431768211456",  # 128-bit
        "-2147483648",
        "-2147483649",  # 31-bit
        "-4294967296",
        "-4294967297",  # 32-bit
        "-9223372036854775808",
        "-9223372036854775809",  # 63-bit
        "-18446744073709551616",
        "-18446744073709551617",  # 64-bit
        "-170141183460469231731687303715884105728",
        "-170141183460469231731687303715884105729",  # 127-bit
        "-340282366920938463463374607431768211456",
        "-340282366920938463463374607431768211457",  # 128-bit
        # one very large number, broken into parts
        "135066410865995223349603216278805969938881475605667027524485143851526510604"
        + "859533833940287150571909441798207282164471551373680419703964191743046496589"
        + "274256239341020864383202110372958725762358509643110564073501508187510676594"
        + "629205563685529475213500852879416377328533906109750544334999811150056977236"
        + "890927563",
        # for good measures, also as a negative number
        "-135066410865995223349603216278805969938881475605667027524485143851526510604"
        + "859533833940287150571909441798207282164471551373680419703964191743046496589"
        + "274256239341020864383202110372958725762358509643110564073501508187510676594"
        + "629205563685529475213500852879416377328533906109750544334999811150056977236"
        + "890927563",
    ],
    "allDoubleVals": [
        "0.0",
        "-0.0",
        "0.111111111111",
        "-0.111111111111",
        "1.0",
        "-1.0",
        "0.00000000000000000000000000001",
        "-0.00000000000000000000000000001",
        "9007199254740991.0",
        "-9007199254740991.0",
        "9007199254740992.0",
        "-9007199254740992.0",
        "-9223372036854775808.0",
        "-9223372036854775809.0",  # 63-bit
        "-18446744073709551616.0",
        "-18446744073709551617.0",  # 64-bit
        "-170141183460469231731687303715884105728.0",
        "-170141183460469231731687303715884105729.0",  # 127-bit
        "-340282366920938463463374607431768211456.0",
        "-340282366920938463463374607431768211457.0",  # 128-bit
    ],
}


def _determine_values(value_set_names, value_sets):
    values = []
    for vals in value_set_names:
        vals = vals.strip()
        if vals in value_sets:
            values = values + value_sets[vals][:]

    if not values:
        raise Exception("Did not find value set named: " + value_set_names)
    return values


def _construct_variable(name: str, value_set_name: List[str], value_sets):
    values = _determine_values(value_set_name, value_sets)
    return _Variable(name, value_set_name, values)


class _Variable:
    def __init__(self, name: str, value_sets_names: List[str], values: List[str]):
        self._name = name
        self._names_of_value_sets = value_sets_names
        self._values = values
        self._regex = re.compile(r"\b" + name + r"\b")

    def get_regex(self):
        return self._regex

    def is_in(self, string):
        return self._regex.search(string) is not None

    def substitute(self, string, value):
        return self._regex.sub(value, string)

    def get_name(self):
        return self._name

    def get_values(self):
        return self._values

    def get_constructor_method_name(self, val_handling: str):
        names = self._names_of_value_sets[:]
        names.sort()

        for i, name in enumerate(names):
            names[i] = name[0].upper() + name[1:]

        name = "".join(names)

        return f"createVector{val_handling}{name}"


class _Specification:
    def __init__(self, name, clazz, spec, value_sets=None, **kwargs):
        self._test_name = name
        self._class_name = clazz
        self._spec = spec

        self._config = kwargs
        self._value_sets = value_sets if value_sets else _DEFAULT_VAL_SETS
        self._test_vars = [
            _construct_variable(name, val_set, self._value_sets)
            for name, val_set in self._config.items()
        ]

    def get_name(self):
        return self._test_name

    def get_class_name(self):
        return self._class_name

    def get_body(self):
        return self._spec

    def get_config(self):
        return self._config

    def append_part(self, spec: str):
        self._spec += spec

    def _process_trivial_tests(self):
        lines = self._spec.split("\n")
        processed_lines = []
        for line in lines:
            if "==" in line:
                parts = line.split("==")
                assert len(parts) == 2
                processed_lines.append(f"self expect: {parts[0]} toBe: {parts[1]}\n")
                continue

            if "=" in line:
                parts = line.split("=")
                assert len(parts) == 2
                processed_lines.append(f"self expect: {parts[0]} toEqual: {parts[1]}\n")
                continue

            if ">" in line:
                parts = line.split(">")
                assert len(parts) == 2
                processed_lines.append(
                    f"self expect: {parts[0]} toBeGreaterThan: {parts[1]}"
                )
                continue

            # skip empty lines
            if line.strip():
                processed_lines.append(line)
        return processed_lines

    @staticmethod
    def _uses_var(var_regex, processed_lines):
        for line in processed_lines:
            if var_regex.is_in(line):
                return True
        return False

    def _gen_literal_permutations(
        self, method, processed_lines, set_vars, var_values, remaining_vars
    ):
        if remaining_vars:
            var = remaining_vars[0]
            remaining_vars = remaining_vars[1:]

            for value in var.get_values():
                self._gen_literal_permutations(
                    method,
                    processed_lines,
                    set_vars + [var],
                    var_values + [value],
                    remaining_vars,
                )
        else:
            for line in processed_lines:
                for v_idx, var in enumerate(set_vars):
                    line = var.substitute(line, var_values[v_idx])
                method.add_statement(Raw(line))
            method.add_statement(Newline())

    def _gen_literal_version(self, clazz, processed_lines):
        for var in self._test_vars:
            assert self._uses_var(var, processed_lines)

        test_name = f"test{self._test_name[0].upper()}{self._test_name[1:]}Literal"
        method = Method(test_name, clazz)

        self._gen_literal_permutations(
            method, processed_lines, [], [], self._test_vars[:]
        )
        return method

    def _gen_loop(self, target_class, processed_lines, val_handling, rand):
        test_vars = self._test_vars[:]

        current_var = test_vars.pop()

        # construct the inner loop block
        inner_loop_block = Block(target_class, [current_var.get_name()])
        for line in processed_lines:
            inner_loop_block.add_statement(Raw(line))

        do_msg = None
        current_block = inner_loop_block
        while current_var:
            values = self._construct_receiver(
                current_var, rand, target_class, val_handling
            )
            do_msg = MsgSend("do:", [values, current_block])

            if test_vars:
                current_var: Optional[_Variable] = test_vars.pop()
                current_block = Block(target_class, [current_var.get_name()])
                current_block.add_statement(do_msg)
            else:
                current_var = None

        test_name = (
            f"test{self._test_name[0].upper()}{self._test_name[1:]}Loop{val_handling}"
        )
        method = Method(test_name, target_class)
        assert do_msg is not None
        method.add_statement(do_msg)
        return method

    @staticmethod
    def _construct_receiver(
        current_var: _Variable, rand, target_class: Class, val_handling: str
    ):
        # construct the receiver, the argument with literal values
        var_values = current_var.get_values()
        if val_handling == "Backwards":
            var_values.reverse()
        elif val_handling == "Shuffled":
            rand.shuffle(var_values)
        elif val_handling == "ShuffledTwice":
            rand.shuffle(var_values)
            rand.shuffle(var_values)
        values = create_vector_or_array(
            [Raw(val) for val in var_values],
            target_class,
            current_var.get_constructor_method_name(val_handling),
        )
        return values

    def serialize(self, target_class, rand):
        processed_lines = self._process_trivial_tests()

        if self._test_vars:
            # if we have variables, we want to generate the following tests
            # - plain all combinations of variables (if more than one)
            #  - as literal code, for easy debugging

            target_class.add_method(
                self._gen_literal_version(target_class, processed_lines)
            )

            # - nested loops over arrays of values
            #  - forward
            target_class.add_method(
                self._gen_loop(target_class, processed_lines, "", rand)
            )

            #  - backward
            target_class.add_method(
                self._gen_loop(target_class, processed_lines, "Backward", rand)
            )
            #  - shuffled once
            target_class.add_method(
                self._gen_loop(target_class, processed_lines, "Shuffled", rand)
            )
            #  - shuffled another time
            target_class.add_method(
                self._gen_loop(target_class, processed_lines, "ShuffledTwice", rand)
            )

        else:
            test_name = f"test{self._test_name[0].upper()}{self._test_name[1:]}"
            method = Method(test_name, target_class)

            for line in processed_lines:
                method.add_statement(Raw(line))
            target_class.add_method(method)


class _FullSpecification:
    def __init__(self, clazz: str, spec: str):
        self._class_name = clazz
        self._spec = spec

    def get_class_name(self):
        return self._class_name

    def get_body(self):
        return self._spec

    def serialize(self, target_class: Class, _rand):
        assert target_class.get_name() == self._class_name
        assert target_class.get_number_of_methods() == 0
        target_class.set_full_spec(self._spec)


class SpecificationTestGenerator:
    def __init__(self):
        self._specs = []

    def get_specifications(self):
        return self._specs

    def add_specification(self, name: str, clazz: str, spec_body: str, spec_type: str, value_sets=None, **kwargs):
        if spec_type == SPEC_PART_MARKER:
            consumed = False
            for spec in self._specs:
                if spec.get_class_name() == clazz and spec.get_name() == name:
                    spec.append_part(spec_body)
                    consumed = True
            if not consumed:
                raise Exception(
                    f"Spec {clazz}.{name} defined as part, but no {clazz}.{name} main spec found.")
        elif spec_type == SPEC_FULL_MARKER:
            self._specs.append(_FullSpecification(clazz, spec_body))
        else:
            self._specs.append(_Specification(name, clazz, spec_body, value_sets, **kwargs))

    def serialize(self, target_directory):
        rand = Random(42)

        # separate specs
        specs = {}
        classes = []
        for spec in self._specs:
            if spec.get_class_name() not in specs:
                specs[spec.get_class_name()] = []
            specs[spec.get_class_name()].append(spec)

        for clazz_name, spec_in_class in specs.items():
            clazz = Class(clazz_name, object_system.Specification, object_system.Empty)
            for spec in spec_in_class:
                spec.serialize(clazz, rand)

            clazz.serialize(target_directory)
            classes.append(clazz)

        self._generate_harness(classes, target_directory)

    @staticmethod
    def _generate_harness(classes, target_directory):
        harness = Class("AllSpecs", object_system.TestHarness, object_system.Empty)

        # override #tests method
        tests_method = Method("tests", harness)
        harness.add_method(tests_method)

        vector = tests_method.get_unused_local()

        tests_method.add_statement(Write(vector, MsgSend("new", [Read("Vector")])))

        for clazz in classes:
            tests_method.add_statement(
                MsgSend("append:", [Read(vector), Read(clazz.get_name())])
            )

        tests_method.add_statement(Return(Read(vector)))

        harness.serialize(target_directory)
