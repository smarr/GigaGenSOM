from som import object_system
from som.clazz import Class


class EntryPointGenerator(object):
    def __init__(self, class_name, entry_method):
        self._class_name = class_name
        self._entry_method = entry_method

    def serialize(self, target_directory):
        clazz = Class(self._class_name, object_system.Object, object_system.Empty)
        clazz.add_method(self._entry_method)

        clazz.serialize(target_directory)
