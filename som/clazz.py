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

    def get_name(self):
        return self._name

    def add_method(self, method):
        if method.get_name() in self._method_dict:
            raise Exception(
                f"{self._name} has more than one method with the name {method.get_name()}")
        self._method_dict[method.get_name()] = method
        self._unserialized_methods.append(method)

    def has_method(self, method_name):
        return method_name in self._method_dict

    def serialize_body(self):
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
