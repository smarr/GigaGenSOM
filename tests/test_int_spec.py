from gen.spec_test_gen import SpecificationTestGenerator
from tests.util import read_file


def test_int_add_spec(tmp_path):
    spec = {
        "clazz": "IntSpec",
        "name": "intAddition",
        "spec": """ 3 + 4 = 7.
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
        "spec": """self expect:  3 + 4.4 toEqual:  7.4 within: 0.00000001.
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
        "int": ["allIntVals"],
        "spec": """int + 1 > int.
                    self expect: int + 1 toBeKindOf: Integer.
                    """,
        "value_sets": {"allIntVals": ["0", "-1", "333"]},
    }

    spec_gen = SpecificationTestGenerator()
    spec_gen.add_specification(**spec)
    spec_gen.serialize(tmp_path)

    expected_output = """IntSpec = Specification (
  testIntAddIncreasesLiteral = (
    self expect: 0 + 1  toBeGreaterThan:  0.
    self expect: 0 + 1 toBeKindOf: Integer.

    self expect: -1 + 1  toBeGreaterThan:  -1.
    self expect: -1 + 1 toBeKindOf: Integer.

    self expect: 333 + 1  toBeGreaterThan:  333.
    self expect: 333 + 1 toBeKindOf: Integer
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
        "int": ["allIntVals"],
        "arg": ["allIntVals", "allDoubleVals"],
        "spec": """int + arg = (arg + int).
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
    self helper_testIntAddSymmetricLiteral1.
    self helper_testIntAddSymmetricLiteral2
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
    self expect: 0 + 0  toEqual:  (0 + 0).
    self expect: 0 + 0 toBeKindOf: 0 class.

    self expect: 0 + -1  toEqual:  (-1 + 0).
    self expect: 0 + -1 toBeKindOf: -1 class.

    self expect: 0 + 333  toEqual:  (333 + 0).
    self expect: 0 + 333 toBeKindOf: 333 class.

    self expect: 0 + 0.0  toEqual:  (0.0 + 0).
    self expect: 0 + 0.0 toBeKindOf: 0.0 class.

    self expect: 0 + -1.2  toEqual:  (-1.2 + 0).
    self expect: 0 + -1.2 toBeKindOf: -1.2 class.

    self expect: 0 + 3.3  toEqual:  (3.3 + 0).
    self expect: 0 + 3.3 toBeKindOf: 3.3 class.

    self expect: -1 + 0  toEqual:  (0 + -1).
    self expect: -1 + 0 toBeKindOf: 0 class.

    self expect: -1 + -1  toEqual:  (-1 + -1).
    self expect: -1 + -1 toBeKindOf: -1 class.

    self expect: -1 + 333  toEqual:  (333 + -1).
    self expect: -1 + 333 toBeKindOf: 333 class.

    self expect: -1 + 0.0  toEqual:  (0.0 + -1).
    self expect: -1 + 0.0 toBeKindOf: 0.0 class
  )

  helper_testIntAddSymmetricLiteral2 = (
    self expect: -1 + -1.2  toEqual:  (-1.2 + -1).
    self expect: -1 + -1.2 toBeKindOf: -1.2 class.

    self expect: -1 + 3.3  toEqual:  (3.3 + -1).
    self expect: -1 + 3.3 toBeKindOf: 3.3 class.

    self expect: 333 + 0  toEqual:  (0 + 333).
    self expect: 333 + 0 toBeKindOf: 0 class.

    self expect: 333 + -1  toEqual:  (-1 + 333).
    self expect: 333 + -1 toBeKindOf: -1 class.

    self expect: 333 + 333  toEqual:  (333 + 333).
    self expect: 333 + 333 toBeKindOf: 333 class.

    self expect: 333 + 0.0  toEqual:  (0.0 + 333).
    self expect: 333 + 0.0 toBeKindOf: 0.0 class.

    self expect: 333 + -1.2  toEqual:  (-1.2 + 333).
    self expect: 333 + -1.2 toBeKindOf: -1.2 class.

    self expect: 333 + 3.3  toEqual:  (3.3 + 333).
    self expect: 333 + 3.3 toBeKindOf: 3.3 class
  )

)"""

    actual_output = read_file(tmp_path, "IntSpec.som").strip()

    # print("333333333")
    # print(actual_output)
    # print("333333333")
    assert expected_output == actual_output
