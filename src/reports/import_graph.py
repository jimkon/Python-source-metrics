import ast

import pandas as pd

from src.python.python_source_obj import PythonSourceObj
from src.visitors.visitor import TreeNodeVisitor


class CollectImportsVisitor(TreeNodeVisitor):
    def __init__(self):
        self._module_imports_list = []

    def visit_module(self, node):
        module_name = node.data.name
        module_imports_list = []
        for _ast in node.data.ast:
            if isinstance(_ast, ast.Import):
                for alias in _ast.names:
                    module_imports_list.append([module_name, alias.name])
            elif isinstance(_ast, ast.ImportFrom):
                for alias in _ast.names:
                    module_imports_list.append([module_name, f"{_ast.module}.{alias.name}"])

        if len(module_imports_list) == 0:
            module_imports_list.append([module_name, 'no-imports'])

        self._module_imports_list.extend(module_imports_list)

    def result(self):
        return pd.DataFrame(self._module_imports_list, columns=['module', 'imports'])


if __name__ == "__main__":
    src_path = r"C:\Users\jim\PycharmProjects\Python-source-metrics\report_files\code_copy\src"
    ps = PythonSourceObj.from_project_source(src_path)
    imports = CollectImportsVisitor()
    ps.use_visitor(imports)
    print(imports.result())
