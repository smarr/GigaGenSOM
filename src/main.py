from gen.entry_point_gen import EntryPointGenerator
from gen.method_gen import create_method_print_string

## Approach, sketch it out first, don't generalize yet

# Scenario 1
# - generate a class with a run method that prints hello world


m_gen = create_method_print_string("run", "Hello World!")
gen = EntryPointGenerator("Hello", m_gen)

gen.serialize("gen_out")
