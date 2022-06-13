import abc
from functools import cached_property

from src.python.basic_structure import *
from src.utils.ast_utils import remove_first_n_characters, analyse_ast
from src.utils.path_utils import dotted_repr_of_path, load_file_as_string
from src.utils.python_file_utils import convert_python_path_to_module_name, validate_python_path


# TODO project object can be a tree node subclass called head (no parent)
# TODO check if tree node get item can be chained example node['src']['utils']['ast_utils]['analyse_ast']
# TODO Init visitor can take argument ex. "functions" and expand only until functions (instead to all the way down to identifiers)


class DirectoryObj(PythonObjData):
    type = "directory"


class ModuleObj(PythonCodeObj):
    type = "module"


class ClassObj(CompoundStatementCodeMixin):
    type = "class"


class FunctionObj(CompoundStatementCodeMixin):
    type = "function"


class ClassMethodObj(FunctionObj):
    type = "class_method"


# class IdentifierObj(PythonCodeObj):
#     type = "identifier"
