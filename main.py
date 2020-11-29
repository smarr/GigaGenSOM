import sys
from argparse import ArgumentParser

from gen.entry_point_gen import EntryPointGenerator
from gen.int_compute_class_gen import IntegerComputationClassGenerator
from gen.method_gen import create_method_print_string

from gen.spec_reader import SpecificationReader

OUTPUT_DIR = "gen_out"

SPEC_DEFAULT = "/Users/smarr/Projects/SOM/SOM.corelib/specification/index.md"

parser = ArgumentParser(description="GigaGenSOM is a SOM source code generator")
parser.add_argument(
    "--spec",
    help="Read SOM specification and generate executable tests.",
    nargs="?",
    metavar="spec-file",
)

parser.add_argument(
    "--int-comp",
    help="Generate integer computation code",
    nargs=2,
    metavar=("callStackHeight", "numMethods"),
    type=int,
)

parser.add_argument(
    "--hello", help="Generates a Hello World program", action="store_true"
)

args = parser.parse_args()

if args.hello:
    m_gen = create_method_print_string("run", None, "Hello World!")
    gen = EntryPointGenerator("Hello", m_gen)
    gen.serialize(OUTPUT_DIR)

if args.int_comp:
    # 3, 10000
    int_gen = IntegerComputationClassGenerator(
        "IntComp", args.int_comp[0], args.int_comp[1]
    )
    int_gen.serialize(OUTPUT_DIR)

if "--spec" in sys.argv:
    spec = SpecificationReader(args.spec or SPEC_DEFAULT)
    spec.read_spec()
    spec.serialize(OUTPUT_DIR)
