import ast
import os.path
from abc import ABC

from src.utils.ast_utils import separate_statement, get_first_ast_of_type
from src.utils.logs import *
from src.utils.path_utils import get_python_files_and_directories


class Visitor(ABC):

    def visit(self, node):
        if node.type == "directory":
            self.visit_directory(node)
        elif node.type == "module":
            self.visit_module(node)
        elif node.type == "class":
            self.visit_class(node)
        elif node.type == "function":
            self.visit_function(node)
        elif node.type == "class_method":
            self.visit_class_method(node)
        else:
            log_yellow(f"Functionality for visiting {node=} of class {node.__class__} is missing.")

    def visit_directory(self, node):
        pass

    def visit_module(self, node):
        pass

    def visit_class(self, node):
        pass

    def visit_function(self, node):
        pass

    def visit_class_method(self, node):
        pass


class PrintVisitor(Visitor):
    def __init__(self):
        self._count = 0

    def _log(self, prefix, node):
        self._count += 1
        log(f"{self._count} |{'   '*(node.get_depth()-1)}+--- {prefix} -> {node.name}", verbosity=1)

    def visit_directory(self, node):
        self._log("Directory", node)

    def visit_module(self, node):
        self._log("Module", node)

    def visit_class(self, node):
        self._log("Class", node)

    def visit_function(self, node):
        self._log("Function", node)

    def visit_class_method(self, node):
        self._log("Class Method", node)


class InitVisitor(Visitor):

    def __init__(self, obj_factory):
        self._obj_factory = obj_factory

    def visit_directory(self, node):
        dir_path = self._obj_factory.calc_filepath(node.filename)
        python_filenames, dir_names = get_python_files_and_directories(dir_path)
        list_objs = []
        for python_file in python_filenames:
            module_obj = self._obj_factory.module(python_file, parent=node)
            log_cyan(f"Extracted module {module_obj.name}", verbosity=3)
            list_objs.append(module_obj)

        for dir_path in dir_names:
            dir_obj = self._obj_factory.directory(dir_path, parent=node)
            log_cyan(f"Extracted directory {dir_obj.name}", verbosity=3)
            list_objs.append(dir_obj)

        node.set_branches(list_objs)
        log_cyan(f"Init Directory:{node.name} branches ({len(list_objs)})", verbosity=3)

    def _fetch_compound_statement(self, from_code, asts_to_fetch, node):
        list_objs = []
        cur_code = from_code
        fetched_ast = get_first_ast_of_type(cur_code, asts_to_fetch.keys())
        while fetched_ast:
            sep_code, remaining_code = separate_statement(cur_code, fetched_ast)
            obj = None
            for _ast_type in asts_to_fetch.keys():
                if isinstance(fetched_ast, _ast_type):
                    obj = asts_to_fetch[_ast_type](node.filename, sep_code, parent=node)
                    log_red(f"Extracted {_ast_type} -> {obj.name}")
                    break

            list_objs.append(obj)
            cur_code = remaining_code
            fetched_ast = get_first_ast_of_type(cur_code, [ast.ClassDef, ast.FunctionDef])
        return list_objs

    def visit_module(self, node):
        asts_to_fetch = {ast.ClassDef: self._obj_factory.class_obj, ast.FunctionDef: self._obj_factory.function}

        list_objs = self._fetch_compound_statement(node.code, asts_to_fetch, node)

        node.set_branches(list_objs)
        log_cyan(f"Init Module:{node.name} branches ({len(list_objs)})", verbosity=3)

    def visit_class(self, node):
        asts_to_fetch = {ast.ClassDef: self._obj_factory.class_obj, ast.FunctionDef: self._obj_factory.class_method}

        list_objs = self._fetch_compound_statement(node.statement_inner_code, asts_to_fetch, node)
        node.set_branches(list_objs)
        log_cyan(f"Init Module:{node.name} branches ({len(list_objs)})", verbosity=3)

