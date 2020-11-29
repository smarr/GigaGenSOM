from gen.spec_test_gen import SpecificationTestGenerator
from gen.spec_types import SPEC_MARKER
from tests.util import read_file


def test_int_add_spec(tmp_path):
    spec = {
        "clazz": "IntSpec",
        "name": "intAddition",
        "spec_type": SPEC_MARKER,
        "spec_body": """ 3 + 4 = 7.
                    -4 + 3 = -1.
                    """,
    }
    spec_gen = SpecificationTestGenerator()
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testIntAddition = (
    self expect:  3 + 4  toEqual:  7.
    self expect:                     -4 + 3  toEqual:  -1
  )

)
"""

    actual_output = read_file(tmp_path, "IntSpec.som")
    assert expected_output == actual_output


def test_double_add_spec(tmp_path):
    spec = {
        "clazz": "IntSpec",
        "name": "doubleAddition",
        "spec_type": SPEC_MARKER,
        "spec_body": """self expect:  3 + 4.4 toEqual:  7.4 within: 0.00000001.
                    self expect: -4 + 3.3 toEqual: -0.7 within: 0.00000001.
                    """,
    }

    spec_gen = SpecificationTestGenerator()
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testDoubleAddition = (
    self expect:  3 + 4.4 toEqual:  7.4 within: 0.00000001.
    self expect: -4 + 3.3 toEqual: -0.7 within: 0.00000001
  )

)
"""

    actual_output = read_file(tmp_path, "IntSpec.som")
    assert expected_output == actual_output


def test_int_add_inc(tmp_path):
    spec = {
        "clazz": "IntSpec",
        "name": "intAddIncreases",
        "spec_type": SPEC_MARKER,
        "int": ["allIntVals"],
        "spec_body": """int + 1 > int.
                    self expect: int + 1 toBeKindOf: Integer.
                    """,
        "value_sets": {"allIntVals": ["0", "-1", "333"]},
    }

    spec_gen = SpecificationTestGenerator()
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testIntAddIncreasesLiteral = (
    | int |
    int := 0.
    self expect: int + 1  toBeGreaterThan:  int.
    self expect: int + 1 toBeKindOf: Integer.

    int := -1.
    self expect: int + 1  toBeGreaterThan:  int.
    self expect: int + 1 toBeKindOf: Integer.

    int := 333.
    self expect: int + 1  toBeGreaterThan:  int.
    self expect: int + 1 toBeKindOf: Integer
  )

  testIntAddIncreasesLoop = (
    #(0 -1 333) do: [:int |
      self expect: int + 1  toBeGreaterThan:  int.
      self expect: int + 1 toBeKindOf: Integer ]
  )

  testIntAddIncreasesLoopBackward = (
    #(0 -1 333) do: [:int |
      self expect: int + 1  toBeGreaterThan:  int.
      self expect: int + 1 toBeKindOf: Integer ]
  )

  testIntAddIncreasesLoopShuffled = (
    #(-1 0 333) do: [:int |
      self expect: int + 1  toBeGreaterThan:  int.
      self expect: int + 1 toBeKindOf: Integer ]
  )

  testIntAddIncreasesLoopShuffledTwice = (
    #(0 -1 333) do: [:int |
      self expect: int + 1  toBeGreaterThan:  int.
      self expect: int + 1 toBeKindOf: Integer ]
  )

)"""

    actual_output = read_file(tmp_path, "IntSpec.som").strip()

    # print("-----------")
    # print(actual_output)
    # print("-----------")

    assert expected_output == actual_output


def test_add_symmetric(tmp_path):
    spec = {
        "clazz": "IntSpec",
        "name": "intAddSymmetric",
        "spec_type": SPEC_MARKER,
        "int": ["allIntVals"],
        "arg": ["allIntVals", "allDoubleVals"],
        "spec_body": """int + arg = (arg + int).
                    self expect: int + arg toBeKindOf: arg class.
                    """,
        "value_sets": {
            "allIntVals": ["0", "-1", "333"],
            "allDoubleVals": ["0.0", "-1.2", "3.3"],
        },
    }

    spec_gen = SpecificationTestGenerator()
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testIntAddSymmetricLiteral = (
    | int arg |
    self helper_testIntAddSymmetricLiteral1.
    self helper_testIntAddSymmetricLiteral2.
    self helper_testIntAddSymmetricLiteral3
  )

  testIntAddSymmetricLoop = (
    #(0 -1 333) do: [:int |
      #(0 -1 333 0.0 -1.2 3.3) do: [:arg |
        self expect: int + arg  toEqual:  (arg + int).
        self expect: int + arg toBeKindOf: arg class ] ]
  )

  testIntAddSymmetricLoopBackward = (
    #(0 -1 333) do: [:int |
      #(0 -1 333 0.0 -1.2 3.3) do: [:arg |
        self expect: int + arg  toEqual:  (arg + int).
        self expect: int + arg toBeKindOf: arg class ] ]
  )

  testIntAddSymmetricLoopShuffled = (
    #(-1 333 0) do: [:int |
      #(0.0 -1 333 -1.2 0 3.3) do: [:arg |
        self expect: int + arg  toEqual:  (arg + int).
        self expect: int + arg toBeKindOf: arg class ] ]
  )

  testIntAddSymmetricLoopShuffledTwice = (
    #(-1 333 0) do: [:int |
      #(3.3 333 0 0.0 -1 -1.2) do: [:arg |
        self expect: int + arg  toEqual:  (arg + int).
        self expect: int + arg toBeKindOf: arg class ] ]
  )

  helper_testIntAddSymmetricLiteral1 = (
    | int arg |
    int := 0.
    arg := 0.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 0.
    arg := -1.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 0.
    arg := 333.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 0.
    arg := 0.0.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 0.
    arg := -1.2.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 0.
    arg := 3.3.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class
  )

  helper_testIntAddSymmetricLiteral2 = (
    | int arg |
    self helper_helper_testIntAddSymmetricLiteral21.
    self helper_helper_testIntAddSymmetricLiteral22
  )

  helper_testIntAddSymmetricLiteral3 = (
    | int arg |
    self helper_helper_testIntAddSymmetricLiteral31.
    self helper_helper_testIntAddSymmetricLiteral32
  )

  helper_helper_testIntAddSymmetricLiteral21 = (
    | int arg |
    int := 0.
    arg := 3.3.
    int := -1.
    arg := 0.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := -1.
    arg := -1.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := -1.
    arg := 333.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := -1.
    arg := 0.0.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := -1.
    arg := -1.2.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class
  )

  helper_helper_testIntAddSymmetricLiteral22 = (
    | int arg |
    int := -1.
    arg := -1.2.
    int := -1.
    arg := 3.3.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class
  )

  helper_helper_testIntAddSymmetricLiteral31 = (
    | int arg |
    int := -1.
    arg := 3.3.
    int := 333.
    arg := 0.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 333.
    arg := -1.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 333.
    arg := 333.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 333.
    arg := 0.0.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class.

    int := 333.
    arg := -1.2.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class
  )

  helper_helper_testIntAddSymmetricLiteral32 = (
    | int arg |
    int := 333.
    arg := -1.2.
    int := 333.
    arg := 3.3.
    self expect: int + arg  toEqual:  (arg + int).
    self expect: int + arg toBeKindOf: arg class
  )

)"""

    actual_output = read_file(tmp_path, "IntSpec.som").strip()

    # print("333333333")
    # print(actual_output)
    # print("333333333")
    assert expected_output == actual_output
