import json
import os.path

from src.configs import PATH_STORE_PYTHON_SOURCE_OBJECTS
from src.python.basic_structure import PythonCodeObj
from src.visitors.visitor import PythonObjVisitor


class SavePythonSourceObj(PythonObjVisitor):
    def __init__(self, to_file):
        self._file_path = os.path.join(PATH_STORE_PYTHON_SOURCE_OBJECTS, to_file)
        self._storage_dict = {}
        pass

    def _add_node(self, name, type, code, branches):
        node_dict = {
            'type': type,
            'code': code,
            'branches': list(branches.keys())
        }
        self._storage_dict[name] = node_dict

    def visit_all(self, node):
        type = node.data.type
        name = node.data.name
        branches = node.branches
        code = node.data.code if issubclass(node.data.__class__, PythonCodeObj) else None
        self._add_node(name, type, code, branches)

    def save(self):
        with open(self._file_path, 'w') as fp:
            json.dump(self._storage_dict, fp, indent=4)

