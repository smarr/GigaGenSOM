from gen.int_compute_class_gen import IntegerComputationClassGenerator
from tests.util import read_file, assert_runs_to_completion


def test_int_comp(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3, 3)
    int_gen.serialize(tmp_path)

    actual_output = read_file(tmp_path, "IntComp.som")

    expected_output = """IntComp = (
  base0: a b: b c: c = (
    | l1 |
    l1 := 9.
    l1 := l1 * c negated.
    l1 := l1 min: (a min: b) + (a * a).
    ^ l1
  )

  base1: a = (
    | l1 |
    l1 := 6.
    l1 := l1 abs.
    l1 := l1 min: a + a.
    l1 := l1 + 387 abs.
    l1 := l1 * (a / 470).
    l1 := l1 * (a % 781 / 867).
    ^ l1
  )

  base2: a = (
    | l1 |
    l1 := 6.
    l1 := l1 negated.
    l1 := l1 min: a negated.
    l1 := l1 negated.
    l1 := l1 + (a * a).
    ^ l1
  )

  method0: a = (
    | l1 |
    l1 := 6.
    l1 := l1 min: (self base1: a).
    l1 := l1 * (self base1: 704).
    l1 := l1 + (self base2: a).
    ^ l1
  )

  method1: a b: b = (
    | l1 |
    l1 := 5.
    l1 := l1 - (self base1: a).
    l1 := l1 min: (self base0: b b: b c: 658).
    ^ l1
  )

  method2: a = (
    | l1 |
    l1 := 10.
    l1 := l1 * (self base1: a).
    ^ l1
  )

  method3: a = (
    | l1 |
    l1 := 3.
    l1 := l1 min: (self method0: 156).
    ^ l1
  )

  method4: a = (
    | l1 |
    l1 := 9.
    l1 := l1 + (self method2: a).
    l1 := l1 min: (self method1: a b: a).
    ^ l1
  )

  method5: a = (
    | l1 |
    l1 := 6.
    l1 := l1 - (self method2: 787).
    ^ l1
  )

  run = (
    | l1 |
    l1 := 5.
    l1 := l1 as32BitSignedValue.
    l1 := l1 min: (self method5: 736).
    l1 := l1 abs.
    l1 := l1 - (self method4: (self method3: 464)).
    ^ l1
  )

)
"""

    assert expected_output == actual_output
    assert_runs_to_completion(tmp_path, "IntComp")
