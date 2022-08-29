from src.python.basic_structure import PythonCodeObj
from src.utils.storage_mixins import StorePythonSourceObj
from src.visitors.visitor import TreeNodeVisitor


class ConvertPythonSourceObjToDict(TreeNodeVisitor):
    def __init__(self):
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

    def dict(self):
        return self._storage_dict

