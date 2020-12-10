from gen.generator import IND


class Class:
    def __init__(self, class_name, super_class, class_class, is_core_class=False):
        self._fields = []
        self._name = class_name

        self._unserialized_methods = []
        self._serialized_methods = []
        self._method_dict = {}

        self._class_comment = None
        self._super_class = super_class
        self._class_class = class_class
        self._is_core_class = is_core_class

        self._full_spec = None

    def get_name(self):
        return self._name

    def get_unused_field(self):
        num_fields = len(self._fields)
        new_field = f"f{(num_fields + 1)}"
        self._fields.append(new_field)
        return new_field

    def add_field_if_not_present(self, field_name):
        if field_name not in self._fields:
            self._fields.append(field_name)
        return field_name

    def add_method(self, method):
        assert self._full_spec is None

        if method.get_name() in self._method_dict:
            raise Exception(
                f"{self._name} has more than one method with the name {method.get_name()}"
            )
        self._method_dict[method.get_name()] = method
        self._unserialized_methods.append(method)

    def has_method(self, method_name):
        return method_name in self._method_dict

    def get_number_of_methods(self):
        return len(self._method_dict)

    def set_full_spec(self, full_spec):
        assert self._full_spec is None
        assert full_spec is not None
        self._full_spec = full_spec

    def serialize_body(self):
        assert self._full_spec is None

        body = ""

        if self._fields:
            body += f"{IND}|"
            for field in self._fields:
                body += f" {field}"
            body += " |\n\n"

        while self._unserialized_methods:
            method = self._unserialized_methods.pop(0)
            method_body = method.serialize()
            if method_body:
                body += method_body
                body += "\n"
            self._serialized_methods.append(method)

        return body

    def _serialize_full_spec(self, file_name):
        assert len(self._method_dict) == 0
        with open(file_name, "w") as target_file:
            target_file.write(self._full_spec)
            target_file.write("\n")

    def serialize(self, target_directory):
        file_name = f"{target_directory}/{self._name}.som"

        if self._full_spec:
            self._serialize_full_spec(file_name)
            return

        super_class_name = self._super_class.get_name()
        if super_class_name == "Object":
            super_class_name = ""
        else:
            super_class_name = super_class_name + " "

        class_definition = f"{self._name} = {super_class_name}(\n"
        class_end = ")\n"
        with open(file_name, "w") as target_file:
            target_file.write(class_definition)

            class_body = self.serialize_body()
            target_file.write(class_body)

            if self._class_class:
                class_class_body = self._class_class.serialize_body()
                if class_class_body:
                    target_file.write(f"{IND}----\n\n")
                    target_file.write(class_class_body)

            target_file.write(class_end)
