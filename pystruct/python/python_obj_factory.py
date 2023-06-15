from pystruct.python.code_structure import *


class PathObjectFactory:

    def __init__(self, root_path):
        self._root_path = root_path

    @property
    def root_path(self):
        return self._root_path

    def directory(self, name, parent=None):
        if not parent:
            path = self._root_path
        else:
            path = parent.data.path[name]

        dir_obj = DirectoryObj(name=name, path=path)
        return TreeNode(parent, data=dir_obj)

    def module(self, name, code, parent=None):
        if not parent:
            path = self._root_path
        else:
            path = parent.data.path[name]

        module_obj = ModuleObj(name, path, code)
        return TreeNode(parent, data=module_obj)

    def import_node(self, name, code, parent=None):
        path = parent.data.path
        import_obj = ImportObj(name, path, code)
        return TreeNode(parent, data=import_obj)

    def class_node(self, name, code, parent=None):
        path = parent.data.path
        class_obj = ClassObj(name, path, code)
        return TreeNode(parent, data=class_obj)

    def function(self, name, code, parent=None):
        path = parent.data.path
        func_obj = FunctionObj(name, path, code)
        return TreeNode(parent, data=func_obj)

    def class_method(self, name, code, parent=None):
        path = parent.data.path
        class_method_obj = ClassMethodObj(name, path, code)
        return TreeNode(parent, data=class_method_obj)


class DictObjectFactory:
    def node_dict_to_object(self, name, node_dict):
        if node_dict['type'] == "directory":
            return DirectoryObj(name=name, path=None)
        elif node_dict['type'] == "module":
            return ModuleObj(name, None, node_dict['code'])
        elif node_dict['type'] == "import":
            return ImportObj(name, None, node_dict['code'])
        elif node_dict['type'] == "class":
            return ClassObj(name, None, node_dict['code'])
        elif node_dict['type'] == "function":
            return FunctionObj(name, None, node_dict['code'])
        elif node_dict['type'] == "class_method":
            return ClassMethodObj(name, None, node_dict['code'])



