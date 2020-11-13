from gen.entry_point_gen import EntryPointGenerator
from gen.int_compute_class_gen import IntegerComputationClassGenerator
from gen.method_gen import create_method_print_string

## Approach, sketch it out first, don't generalize yet

# Scenario 1
# - generate a class with a run method that prints hello world

OUTPUT_DIR = "gen_out"

m_gen = create_method_print_string("run", "Hello World!")
gen = EntryPointGenerator("Hello", m_gen)

gen.serialize(OUTPUT_DIR)

int_gen = IntegerComputationClassGenerator("IntComp", 3)
int_gen.serialize(OUTPUT_DIR)
