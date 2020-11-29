import sys

from gen.spec_test_gen import SpecificationTestGenerator

_SPEC_MARKER = "```{spec "
_END_FENCE = "```"


class ParseError(Exception):
    def __init__(self, msg, line_no, line_text):
        super().__init__()
        self.msg = msg
        self.line_no = line_no
        self.line_text = line_text


class SpecificationReader:
    def __init__(self, file_path, input_str=None):
        self._file_path = file_path
        self._input_str = input_str

        # should only have one set
        assert (file_path and not input_str) or (not file_path and input_str)

        self._spec_gen = SpecificationTestGenerator()
        self._class_method_dict = {}

    def get_specs(self):
        return self._spec_gen.get_specifications()

    def serialize(self, target_directory):
        self._spec_gen.serialize(target_directory)

    def read_spec(self):
        try:
            if self._file_path:
                with open(self._file_path, "r") as output_file:
                    self._process_spec(output_file)
            else:
                self._process_spec(self._input_str.split("\n"))
        except ParseError as parse_e:
            if self._file_path:
                file_path = self._file_path
            else:
                file_path = "<str>"
            print(
                f"{file_path}:{parse_e.line_no}: {parse_e.msg}\n\t{parse_e.line_text}",
                file=sys.stderr,
            )
            sys.exit(1)

    def _process_spec(self, lines):
        spec_lines = []
        collect_lines = False

        for i, line in enumerate(lines):
            trimmed = line.lstrip()
            if trimmed.startswith(_SPEC_MARKER):
                collect_lines = True
            elif trimmed.startswith(_END_FENCE):
                collect_lines = False
                self._parse_spec(spec_lines, i + 1)
                spec_lines = []

            if collect_lines:
                spec_lines.append(line)

        assert (
            not spec_lines
        ), "We expect specs to be closed, and thus no spec_lines here"

    def _parse_spec(self, spec_lines, start_line):
        spec_header = spec_lines[0]
        spec_body = "\n".join(spec_lines[1:])

        name, clazz, remaining_args = self._parse_header(spec_header, start_line)

        if clazz not in self._class_method_dict:
            self._class_method_dict[clazz] = {}
        if name in self._class_method_dict[clazz]:
            raise ParseError(
                f"There are multiple {clazz}.{name} specifications",
                start_line,
                spec_header,
            )

        self._class_method_dict[clazz][name] = True
        self._spec_gen.add_specification(name, clazz, spec_body, **remaining_args)

    def _parse_header(self, spec_header, line_no):
        assert spec_header.startswith(_SPEC_MARKER)
        remaining_spec = spec_header[len(_SPEC_MARKER) :]
        remaining_spec, clazz = self._parse_class(remaining_spec, line_no, spec_header)
        remaining_spec, name = self._parse_name(remaining_spec)
        remaining_spec, remaining_args = self._parse_remaining_args(remaining_spec)
        if remaining_spec.strip() != "}":
            raise ParseError(  # pylint: disable=raising-format-tuple
                "The specification is expected to start with `{` and end with `}`.",
                line_no,
                spec_header,
            )

        args = {}
        for (key, value) in remaining_args:
            args[key] = value

        return name, clazz, args

    @staticmethod
    def _parse_class(spec, line_no, full_line):
        dot_idx = spec.find(".")
        if dot_idx < 1:
            raise ParseError(
                "Expected class to be part of spec name. It uses the `class.method` notation.",
                line_no,
                full_line,
            )
        assert dot_idx > 1

        clazz = spec[:dot_idx]
        remaining_spec = spec[dot_idx + 1 :]
        return remaining_spec, clazz.strip()

    @staticmethod
    def _parse_name(spec):
        name_end = spec.find(",")
        if name_end == -1:
            name_end = spec.find("}")

        assert name_end > 1
        name = spec[:name_end]
        if spec[name_end] == ",":
            name_end += 1
        remaining_spec = spec[name_end:]
        return remaining_spec, name.strip()

    def _parse_remaining_args(self, spec):
        equal_idx = spec.find("=")
        if equal_idx == -1:
            return spec, []

        var_name = spec[:equal_idx].strip()
        remaining_spec = spec[equal_idx + 1 :]

        if remaining_spec[0] == "{":
            group_end = remaining_spec.find("}")
            values = remaining_spec[1:group_end].split(",")
            values = [v.strip() for v in values]
            remaining_spec = remaining_spec[group_end + 1 :].strip()
            if remaining_spec[0] == ",":
                remaining_spec = remaining_spec[1:]
        else:
            val_end = remaining_spec.find(",")
            if val_end == -1:
                val_end = remaining_spec.find("}")

            assert val_end > 1
            values = [remaining_spec[:val_end].strip()]
            if remaining_spec[val_end] == ",":
                val_end += 1
            remaining_spec = remaining_spec[val_end:]

        remaining_spec, remaining_args = self._parse_remaining_args(remaining_spec)
        return remaining_spec, [(var_name, values)] + remaining_args
