import ast

import pandas as pd

from src.configs import PATH_STORE_IMPORTS_DICT
from src.utils.storage_mixins import StoreJSON, StoreCSV
from src.visitors.visitor import TreeNodeVisitor


class ImportGraphVisitor(TreeNodeVisitor, StoreCSV):
    def __init__(self):
        self._module_imports_list = []

    def visit_module(self, node):
        for _ast in node.data.ast:
            if isinstance(_ast, ast.Import):
                for alias in _ast.names:
                    self._module_imports_list.append([node.data.name, alias.name])
            elif isinstance(_ast, ast.ImportFrom):
                for alias in _ast.names:
                    self._module_imports_list.append([node.data.name, f"{_ast.module}.{alias.name}"])

    def path_to_store(self):
        return PATH_STORE_IMPORTS_DICT

    def data_to_store(self):
        return pd.DataFrame(self._module_imports_list, columns=['module', 'imports'])
