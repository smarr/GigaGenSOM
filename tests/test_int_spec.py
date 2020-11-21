from gen.spec_test_gen import SpecificationTestGenerator


def test_int_add_spec(tmp_path):
    spec = {"name": "intAddition",
            "spec": """ 3 + 4 = 7.
                    -4 + 3 = -1.
                    """}
    spec_gen = SpecificationTestGenerator("IntSpec")
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testIntAddition = (
    self expect:  3 + 4  toEqual:  7.
    self expect:                     -4 + 3  toEqual:  -1
  )

)
"""

    with open(str(tmp_path) + "/IntSpec.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    assert expected_output == actual_output


def test_double_add_spec(tmp_path):
    spec = {"name": "doubleAddition",
            "spec": """self expect:  3 + 4.4 toEqual:  7.4 within: 0.00000001.
                    self expect: -4 + 3.3 toEqual: -0.7 within: 0.00000001.
                    """}

    spec_gen = SpecificationTestGenerator("IntSpec")
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testDoubleAddition = (
    self expect:  3 + 4.4 toEqual:  7.4 within: 0.00000001.
    self expect: -4 + 3.3 toEqual: -0.7 within: 0.00000001
  )

)
"""

    with open(str(tmp_path) + "/IntSpec.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    assert expected_output == actual_output


def test_int_add_inc(tmp_path):
    spec = {"name": "intAddIncreases",
            "int": "allIntVals",
            "spec": """int + 1 > int.
                    self expect: int + 1 toBeKindOf: Integer.
                    """}

    spec_gen = SpecificationTestGenerator("IntSpec")
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testIntAddIncreasesLiteral = (
    self expect: 0 + 1  toBeGreaterThan:  0.
    self expect: 0 + 1 toBeKindOf: Integer.

    self expect: -0 + 1  toBeGreaterThan:  -0.
    self expect: -0 + 1 toBeKindOf: Integer.

    self expect: 1 + 1  toBeGreaterThan:  1.
    self expect: 1 + 1 toBeKindOf: Integer.

    self expect: 10 + 1  toBeGreaterThan:  10.
    self expect: 10 + 1 toBeKindOf: Integer.

    self expect: 200 + 1  toBeGreaterThan:  200.
    self expect: 200 + 1 toBeKindOf: Integer.

    self expect: -1 + 1  toBeGreaterThan:  -1.
    self expect: -1 + 1 toBeKindOf: Integer.

    self expect: -10 + 1  toBeGreaterThan:  -10.
    self expect: -10 + 1 toBeKindOf: Integer.

    self expect: -200 + 1  toBeGreaterThan:  -200.
    self expect: -200 + 1 toBeKindOf: Integer.

    self expect: 255 + 1  toBeGreaterThan:  255.
    self expect: 255 + 1 toBeKindOf: Integer.

    self expect: 256 + 1  toBeGreaterThan:  256.
    self expect: 256 + 1 toBeKindOf: Integer.

    self expect: 65535 + 1  toBeGreaterThan:  65535.
    self expect: 65535 + 1 toBeKindOf: Integer.

    self expect: 65536 + 1  toBeGreaterThan:  65536.
    self expect: 65536 + 1 toBeKindOf: Integer.

    self expect: 2147483647 + 1  toBeGreaterThan:  2147483647.
    self expect: 2147483647 + 1 toBeKindOf: Integer.

    self expect: 2147483648 + 1  toBeGreaterThan:  2147483648.
    self expect: 2147483648 + 1 toBeKindOf: Integer.

    self expect: 4294967295 + 1  toBeGreaterThan:  4294967295.
    self expect: 4294967295 + 1 toBeKindOf: Integer.

    self expect: 4294967296 + 1  toBeGreaterThan:  4294967296.
    self expect: 4294967296 + 1 toBeKindOf: Integer.

    self expect: 9223372036854775807 + 1  toBeGreaterThan:  9223372036854775807.
    self expect: 9223372036854775807 + 1 toBeKindOf: Integer.

    self expect: 9223372036854775808 + 1  toBeGreaterThan:  9223372036854775808.
    self expect: 9223372036854775808 + 1 toBeKindOf: Integer.

    self expect: 18446744073709551615 + 1  toBeGreaterThan:  18446744073709551615.
    self expect: 18446744073709551615 + 1 toBeKindOf: Integer.

    self expect: 18446744073709551616 + 1  toBeGreaterThan:  18446744073709551616.
    self expect: 18446744073709551616 + 1 toBeKindOf: Integer.

    self expect: 170141183460469231731687303715884105727 + 1  toBeGreaterThan:  170141183460469231731687303715884105727.
    self expect: 170141183460469231731687303715884105727 + 1 toBeKindOf: Integer.

    self expect: 170141183460469231731687303715884105728 + 1  toBeGreaterThan:  170141183460469231731687303715884105728.
    self expect: 170141183460469231731687303715884105728 + 1 toBeKindOf: Integer.

    self expect: 340282366920938463463374607431768211455 + 1  toBeGreaterThan:  340282366920938463463374607431768211455.
    self expect: 340282366920938463463374607431768211455 + 1 toBeKindOf: Integer.

    self expect: 340282366920938463463374607431768211456 + 1  toBeGreaterThan:  340282366920938463463374607431768211456.
    self expect: 340282366920938463463374607431768211456 + 1 toBeKindOf: Integer.

    self expect: -256 + 1  toBeGreaterThan:  -256.
    self expect: -256 + 1 toBeKindOf: Integer.

    self expect: -257 + 1  toBeGreaterThan:  -257.
    self expect: -257 + 1 toBeKindOf: Integer.

    self expect: -65536 + 1  toBeGreaterThan:  -65536.
    self expect: -65536 + 1 toBeKindOf: Integer.

    self expect: -65537 + 1  toBeGreaterThan:  -65537.
    self expect: -65537 + 1 toBeKindOf: Integer.

    self expect: -2147483648 + 1  toBeGreaterThan:  -2147483648.
    self expect: -2147483648 + 1 toBeKindOf: Integer.

    self expect: -2147483649 + 1  toBeGreaterThan:  -2147483649.
    self expect: -2147483649 + 1 toBeKindOf: Integer.

    self expect: -4294967296 + 1  toBeGreaterThan:  -4294967296.
    self expect: -4294967296 + 1 toBeKindOf: Integer.

    self expect: -4294967297 + 1  toBeGreaterThan:  -4294967297.
    self expect: -4294967297 + 1 toBeKindOf: Integer.

    self expect: -9223372036854775808 + 1  toBeGreaterThan:  -9223372036854775808.
    self expect: -9223372036854775808 + 1 toBeKindOf: Integer.

    self expect: -9223372036854775809 + 1  toBeGreaterThan:  -9223372036854775809.
    self expect: -9223372036854775809 + 1 toBeKindOf: Integer.

    self expect: -18446744073709551616 + 1  toBeGreaterThan:  -18446744073709551616.
    self expect: -18446744073709551616 + 1 toBeKindOf: Integer.

    self expect: -18446744073709551617 + 1  toBeGreaterThan:  -18446744073709551617.
    self expect: -18446744073709551617 + 1 toBeKindOf: Integer.

    self expect: -170141183460469231731687303715884105728 + 1  toBeGreaterThan:  -170141183460469231731687303715884105728.
    self expect: -170141183460469231731687303715884105728 + 1 toBeKindOf: Integer.

    self expect: -170141183460469231731687303715884105729 + 1  toBeGreaterThan:  -170141183460469231731687303715884105729.
    self expect: -170141183460469231731687303715884105729 + 1 toBeKindOf: Integer.

    self expect: -340282366920938463463374607431768211456 + 1  toBeGreaterThan:  -340282366920938463463374607431768211456.
    self expect: -340282366920938463463374607431768211456 + 1 toBeKindOf: Integer.

    self expect: -340282366920938463463374607431768211457 + 1  toBeGreaterThan:  -340282366920938463463374607431768211457.
    self expect: -340282366920938463463374607431768211457 + 1 toBeKindOf: Integer.

    self expect: 135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563-135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563 + 1  toBeGreaterThan:  135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563-135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563.
    self expect: 135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563-135066410865995223349603216278805969938881475605667027524485143851526510604859533833940287150571909441798207282164471551373680419703964191743046496589274256239341020864383202110372958725762358509643110564073501508187510676594629205563685529475213500852879416377328533906109750544334999811150056977236890927563 + 1 toBeKindOf: Integer.


  )

)
"""

    with open(str(tmp_path) + "/IntSpec.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    assert expected_output == actual_output


def test_add_symmetric(tmp_path):
    spec = {"name": "intAddSymmetric",
            "int": "allIntVals",
            "arg": "{allIntVals, allDoubleVals}",
            "spec": """int + arg = (arg + int).
                    self expect: int + arg toBeKindOf: arg class.
                    """}

    spec_gen = SpecificationTestGenerator("IntSpec")
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = ""

    with open(str(tmp_path) + "/IntSpec.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    print("333333333")
    print(actual_output)
    print("333333333")
    assert expected_output == actual_output
