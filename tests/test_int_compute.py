from gen.int_compute_class_gen import IntegerComputationClassGenerator


def test_int_comp(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3, 3)
    int_gen.serialize(tmp_path)

    with open(str(tmp_path) + "/IntComp.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    expected_output = """IntComp = (
  base0: a b: b c: c = (
    ^ c / 4383 % (5564 - c abs + 9) + (c / 2665) * b abs max: a abs % (a - a + 7) % (b + 11)
  )

  base1: a b: b = (
    ^ (b max: 2853) % (a abs * b + 7) - (a - a abs - a)
  )

  base2: a b: b = (
    ^ a - 7567 - b % (966 abs - a * 5205 + 11)
  )

  method0: a b: b = (
    ^ (self base2: 6966 b: a) / ((self base1: (self base0: a b: b c: b) b: b) + 10)
  )

  method1: a b: b = (
    ^ (self base2: 2977 b: a) + (self base1: a b: 4365) % ((self base0: 5623 b: b c: b) + 7)
  )

  method2: a b: b = (
    ^ self base2: (self base1: (self base0: b b: 5088 c: b) b: b) b: a
  )

  method3: a b: b = (
    ^ (self method2: 3345 b: b) / ((self method1: 6982 b: 8885) + 11) / ((self method0: 2755 b: b) + 10)
  )

  method4: a b: b = (
    ^ self method2: (self method1: (self method0: a b: a) b: b) b: b
  )

  method5: a b: b = (
    ^ (self method2: a b: 9490) / ((self method1: b b: b) + 9) - (self method0: a b: b)
  )

  run = (
    ^ (self method5: (self method4: 937 b: 1662) b: 1840) - (self method3: 7112 b: 6785)
  )

)
"""

    assert expected_output == actual_output
