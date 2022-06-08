import ast
from abc import ABC, abstractmethod

from src.utils.ast_utils import separate_statement, get_first_ast_of_type
from src.utils.logs import *
from src.utils.path_utils import get_python_files_and_directories, load_file_as_string
from src.utils.python_file_utils import is_python_file


class AbstractVisitor(ABC):
    @abstractmethod
    def visit(self, node):
        pass


class TreeNodeVisitor(AbstractVisitor):

    def visit(self, node):
        self.visit_all(node)
        if node.data.type == "directory":
            self.visit_directory(node)
        elif node.data.type == "module":
            self.visit_module(node)
        elif node.data.type == "class":
            self.visit_class(node)
        elif node.data.type == "function":
            self.visit_function(node)
        elif node.data.type == "class_method":
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

    def visit_all(self, node):
        pass


class VisitedMixin:
    def _node(self):
        return self

    def accept(self, visitor):
        visitor.visit(self._node())


class PrintPythonObjVisitor(TreeNodeVisitor):
    def __init__(self):
        self._count = 0

    def _log(self, prefix, node):
        self._count += 1
        log(f"{self._count} |{'   '*(node.depth-1)}+--- {prefix} -> {node.data.name}", verbosity=1)

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

    # def visit_object_type(self, node, type):
    #     if issubclass(node, type):
    #         pass



