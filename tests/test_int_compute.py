from gen.int_compute_class_gen import IntegerComputationClassGenerator


def test_int_comp(tmp_path):
    int_gen = IntegerComputationClassGenerator("IntComp", 3)
    int_gen.serialize(tmp_path)

    with open(str(tmp_path) + "/IntComp.som", "r") as output_file:
        actual_output = "".join(output_file.readlines())

    expected_output = """IntComp = (
  base0: a b: b c: c = (
    ^ ((c) abs) % ((a) - (b))
  )

  base1: a = (
    ^ (a) + (9195)
  )

  base2: a = (
    ^ (a) % (9654)
  )

  method0: a = (
    ^ ((self) base2: (5514)) + ((self) base1: (((self) base0: 2615 b: a c: a )))
  )

  method1: a = (
    ^ ((self) base2: (a)) + ((self) base1: (((self) base0: a b: a c: a )))
  )

  method2: a = (
    ^ (((self) base2: (a)) % ((self) base1: (5925))) + (((self) base0: a b: a c: a ))
  )

  method3: a = (
    ^ (self) base2: ((self) base2: ((self) base2: (a)))
  )

  method4: a = (
    ^ (((self) base2: (a)) * ((self) base2: (a))) - ((self) base2: (a))
  )

  method5: a = (
    ^ ((self) base2: ((self) base2: (a))) - ((self) base2: (1169))
  )

  run = (
    ^ ((self) base2: (916)) - ((self) base2: ((self) base2: (9125)))
  )

)
"""

    assert expected_output == actual_output
