from gen.int_compute_class_gen import IntegerComputationClassGenerator
from tests.util import read_file, assert_runs_to_completion


def test_int_comp(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3, 3)
    int_gen.serialize(tmp_path)

    actual_output = read_file(tmp_path, "IntComp.som").strip()

    expected_output = """IntComp = (
  | l1 |

  getL1 = (
    ^ l1
  )

  base0: a b: b c: c = (
    l1 := 9.
    l1 := l1 * c negated.
    l1 := l1 abs.
    l1 := l1 - ((a min: b) + (a - a)).
    l1 := (l1 min: 1) max: -3.
    ^ l1
  )

  base1: a b: b c: c d: d = (
    l1 := 4.
    l1 := l1 negated.
    l1 := l1 + (a min: 295).
    l1 := l1 - (40 + c).
    l1 := l1 * (d * b - b).
    l1 := l1 + (172 - d).
    l1 := (l1 min: 30) max: -88.
    ^ l1
  )

  base2: a b: b = (
    l1 := 10.
    l1 := l1 negated.
    l1 := l1 abs.
    l1 := l1 - a as32BitSignedValue.
    l1 := l1 abs.
    l1 := l1 - (b negated * a).
    l1 := (l1 min: 82) max: -12.
    ^ l1
  )

  method0: a b: b = (
    l1 := 10.
    l1 := l1 * (self base1: (self base0: (self base2: a b: 161) b: a c: 234) b: b c: b d: b).
    l1 := (l1 min: 75) max: -49.
    ^ l1
  )

  method1: a b: b c: c = (
    l1 := 9.
    l1 := l1 as32BitSignedValue.
    l1 := l1 + (self base1: b b: a c: c d: b).
    l1 := l1 min: (self base0: a b: 216 c: c).
    l1 := (l1 min: 88) max: -32.
    ^ l1
  )

  method2: a b: b c: c d: d = (
    l1 := 9.
    l1 := l1 as32BitSignedValue.
    l1 := l1 as32BitSignedValue.
    l1 := l1 * (self base1: c b: a c: 134 d: 91).
    l1 := (l1 min: 82) max: -36.
    ^ l1
  )

  method3: a b: b c: c = (
    l1 := 4.
    l1 := l1 + (self method2: c b: b c: b d: 157).
    l1 := (l1 min: 73) max: -90.
    ^ l1
  )

  method4: a b: b = (
    l1 := 8.
    l1 := l1 as32BitSignedValue.
    l1 := l1 - (self method0: 272 b: 65).
    l1 := (l1 min: 68) max: -23.
    ^ l1
  )

  method5: a b: b c: c = (
    l1 := 6.
    l1 := l1 abs.
    l1 := l1 abs.
    l1 := l1 + (self method1: c b: a c: b).
    l1 := (l1 min: 29) max: -92.
    ^ l1
  )

  run = (
    l1 := 10.
    l1 := l1 negated.
    l1 := l1 - (self method5: (self method4: (self method3: 283 b: 112 c: 30) b: 169) b: 248 c: 67).
    l1 := (l1 min: 61) max: -48.
    l1 println
  )

)"""

    assert expected_output == actual_output
    assert_runs_to_completion(tmp_path, "IntComp")


def test_int_comp_large(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3, 45)
    int_gen.serialize(tmp_path)
    assert_runs_to_completion(tmp_path, "IntComp")
