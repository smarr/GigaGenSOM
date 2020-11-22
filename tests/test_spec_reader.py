from gen.spec_reader import SpecificationReader


def test_basic_spec():
    input_str = """
Test

```{spec IntSpec.intAddition}
 3 + 4 = 7.
-4 + 3 = -1.
```

"""
    reader = SpecificationReader(None, input_str)
    reader.read_spec()
    specs = reader.get_specs()

    assert len(specs) == 1
    spec = specs[0]

    assert spec.get_name() == "intAddition"
    assert spec.get_class_name() == "IntSpec"
    assert spec.get_body() == """ 3 + 4 = 7.
-4 + 3 = -1."""


def test_two_specs():
    input_str = """
Spec 1

```{spec IntSpec1.doubleAddition}
self expect:  3 + 4.4 toEqual:  7.4 within: 0.00000001.
self expect: -4 + 3.3 toEqual: -0.7 within: 0.00000001.
```

Furthermore, the following should hold for `int` being any integer value:

```{spec IntSpec2.intAddIncreases, int=allIntVals}
int + 1 > int.
self expect: int + 1 toBeKindOf: Integer.
```"""

    reader = SpecificationReader(None, input_str)
    reader.read_spec()

    specs = reader.get_specs()

    assert len(specs) == 2

    assert specs[0].get_name() == "doubleAddition"
    assert specs[0].get_class_name() == "IntSpec1"

    assert specs[1].get_name() == "intAddIncreases"
    assert specs[1].get_class_name() == "IntSpec2"

    assert "int" in specs[1].get_config()
    assert specs[1].get_config()["int"] == ["allIntVals"]


def test_arg_with_two_value_sets():
    input_str = """
And of course, we also expect the following to hold:

```{spec Test.intAddSymmetric, int=allIntVals, arg={allIntVals, allDoubleVals}}
int + arg = (arg + int).
self expect: int + arg toBeKindOf: arg class.
```
"""
    reader = SpecificationReader(None, input_str)
    reader.read_spec()

    specs = reader.get_specs()

    assert len(specs) == 1

    assert specs[0].get_name() == "intAddSymmetric"
    assert specs[0].get_class_name() == "Test"

    assert "int" in specs[0].get_config()
    assert specs[0].get_config()["int"] == ["allIntVals"]

    assert len(specs[0].get_config()) == 2

    assert "int" in specs[0].get_config()
    value_sets = specs[0].get_config()["arg"]

    assert len(value_sets) == 2
    assert value_sets[0] == "allIntVals"
    assert value_sets[1] == "allDoubleVals"
