import abc
from functools import cached_property

from src.python.basic_structure import *
from src.utils.ast_utils import remove_first_n_characters, analyse_ast
from src.utils.path_utils import dotted_repr_of_path, load_file_as_string
from src.utils.python_file_utils import convert_python_path_to_module_name, validate_python_path


# TODO project object can be a tree node subclass called head (no parent)
# TODO check if tree node get item can be chained example node['src']['utils']['ast_utils]['analyse_ast']
# TODO Init visitor can take argument ex. "functions" and expand only until functions (instead to all the way down to identifiers)


class DirectoryObj(TreeNode):
    type = "directory"

    @cached_property
    def name(self):
        return dotted_repr_of_path(self.filename)

    def __str__(self):
        branches_str = ', '.join(list(self.branches.keys())) if self.branches else "<no branches>"
        return f"{self.name}: Directory \"{self.filename}\" branching in [{branches_str}]"


class ModuleObj(TreeNode, CodeObjMixin):
    type = "module"

    def __init__(self, filename, code, parent=None):
        super().__init__(filename, parent)
        self.__code = code

    @cached_property
    def name(self):
        return convert_python_path_to_module_name(self.filename)

    @cached_property
    def code(self) -> str:
        return self.__code

    def __str__(self):
        return f"{self.name}: Module {self.filename} code in \"{self.code_lines[0]}\""


class ClassObj(TreeNode, CompoundStatementCodeMixin):
    type = "class"

    def __init__(self, filename, code, parent=None):
        super().__init__(filename, parent)
        self.__code = code

    @cached_property
    def name(self):
        return f"{self.parent.name if self.parent else ''}.{self.ast[1].name}"

    @cached_property
    def code(self) -> str:
        return self.__code

    def __str__(self):
        return f"{self.name}: Class {self.filename} code in \"{self.code_lines[0]}\""


class FunctionObj(TreeNode, CompoundStatementCodeMixin):
    type = "function"

    def __init__(self, filename, code, parent=None):
        super().__init__(filename, parent)
        self.__code = code

    @cached_property
    def name(self):
        return f"{self.parent.name if self.parent else ''}.{self.ast[1].name}"

    @cached_property
    def code(self) -> str:
        return self.__code

    def __str__(self):
        return f"{self.name}: Function {self.filename} code in \"{self.code_lines[0]}\""


class ClassMethodObj(FunctionObj):
    type = "class_method"

    def __str__(self):
        return f"{self.name}: Class method {self.filename} code in \"{self.code_lines[0]}\""


class IdentifierObj(TreeNode, CodeObjMixin):
    def name(self):
        pass

    type = "identifier"

    def __str__(self):
        return f"{self.name}: Identifier {self.filename} code in \"{self.code_lines[0]}\""
