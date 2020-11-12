from gen.generator import IND


class Class:
    def __init__(self, class_name, super_class, class_class, is_core_class=False):
        self._fields = []
        self._name = class_name
        self._methods = []
        self._class_comment = None
        self._super_class = super_class
        self._class_class = class_class
        self._is_core_class = is_core_class

    def get_name(self):
        return self._name

    def add_method(self, method):
        self._methods.append(method)

    def serialize_body(self):
        body = ""

        if self._fields:
            body += f"{IND}|"
            for field in self._fields:
                body += f" {field}"
            body += " |\n\n"

        for method in self._methods:
            method_body = method.serialize()
            if method_body:
                body += method_body
                body += "\n"

        return body

    def serialize(self, target_directory):
        file_name = f"{target_directory}/{self._name}.som"
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
