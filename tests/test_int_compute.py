from gen.int_compute_class_gen import IntegerComputationClassGenerator
from tests.util import read_file, assert_runs_to_completion


def test_int_comp(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3, 3)
    int_gen.serialize(tmp_path)

    actual_output = read_file(tmp_path, "IntComp.som").strip()

    expected_output = """IntComp = (
  | l1 |

  base0: a b: b c: c = (
    l1 := 9.
    l1 := l1 * c negated.
    l1 := l1 abs.
    l1 := l1 - ((a min: b) + (a - a)).
    ^ l1
  )

  base1: a b: b c: c d: d = (
    l1 := 1.
    l1 := l1 negated.
    l1 := l1 min: a negated.
    l1 := l1 as32BitSignedValue.
    l1 := l1 min: d * 370.
    l1 := l1 as32BitSignedValue.
    l1 := l1 * (d * (b + c)) abs as32BitSignedValue.
    l1 := l1 abs.
    l1 := l1 min: b * 344.
    ^ l1
  )

  base2: a = (
    l1 := 2.
    l1 := l1 negated.
    l1 := l1 - (a * 699).
    ^ l1
  )

  method0: a = (
    l1 := 9.
    l1 := l1 - (self base2: a).
    ^ l1
  )

  method1: a b: b = (
    l1 := 5.
    l1 := l1 + (self base1: (self base0: b b: 580 c: 322) b: b c: 658 d: a).
    ^ l1
  )

  method2: a b: b c: c d: d = (
    l1 := 2.
    l1 := l1 min: (self base1: 408 b: c c: 141 d: d).
    ^ l1
  )

  method3: a b: b = (
    l1 := 2.
    l1 := l1 * (self method2: a b: b c: a d: a).
    l1 := l1 - (self method1: 696 b: b).
    l1 := l1 + (self method0: 881).
    ^ l1
  )

  method4: a b: b = (
    l1 := 5.
    l1 := l1 - (self method1: (self method1: (self method2: a b: b c: 944 d: b) b: a) b: 899).
    ^ l1
  )

  method5: a b: b = (
    l1 := 2.
    l1 := l1 as32BitSignedValue.
    l1 := l1 abs.
    l1 := l1 + (self method1: a b: a).
    ^ l1
  )

  run = (
    l1 := 5.
    l1 := l1 * (self method5: 773 b: 205).
    l1 := l1 negated.
    l1 := l1 * (self method4: 621 b: 216).
    l1 := l1 as32BitSignedValue.
    l1 := l1 abs.
    l1 := l1 - (self method3: 969 b: 271).
    l1 println
  )

)"""

    assert expected_output == actual_output
    assert_runs_to_completion(tmp_path, "IntComp")


def test_int_comp_large(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3, 45)
    int_gen.serialize(tmp_path)
    assert_runs_to_completion(tmp_path, "IntComp")
