import ast

from src.configs import PATH_STORE_IMPORTS_DICT
from src.utils.storage_mixins import StoreJSON
from src.visitors.visitor import TreeNodeVisitor


class ImportGraphVisitor(TreeNodeVisitor, StoreJSON):
    def __init__(self):
        self._module_imports_dict = {}

    def visit_module(self, node):
        _import_list = []
        for _ast in node.data.ast:
            if isinstance(_ast, ast.Import):
                for alias in _ast.names:
                    _import_list.append(alias.name)
            elif isinstance(_ast, ast.ImportFrom):
                for alias in _ast.names:
                    _import_list.append(f"{_ast.module}.{alias.name}")

        self._module_imports_dict[node.data.name] = _import_list

    def path_to_store(self):
        return PATH_STORE_IMPORTS_DICT

    def data_to_store(self):
        return self._module_imports_dict
