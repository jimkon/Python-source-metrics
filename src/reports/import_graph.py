import ast

import pandas as pd

from src.configs import PATH_STORE_IMPORTS_DICT
from src.python.python_source_obj import PythonSourceObj
from src.utils.storage_mixins import StoreJSON, StoreCSV
from src.visitors.visitor import TreeNodeVisitor


class CollectImportsVisitor(TreeNodeVisitor):
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

    def result(self):
        return pd.DataFrame(self._module_imports_list, columns=['module', 'imports'])


if __name__ == "__main__":
    src_path = r"C:\Users\jim\PycharmProjects\Python-source-metrics\report_files\code_copy\src"
    ps = PythonSourceObj.from_project_source(src_path)
    imports = CollectImportsVisitor()
    ps.use_visitor(imports)
    print(imports.result())
