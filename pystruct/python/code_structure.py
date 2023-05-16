from pystruct.python.basic_structure import *


# TODO project object can be a tree node subclass called head (no parent)
# TODO check if tree node get item can be chained example node['pystruct']['utils']['ast_utils]['analyse_ast']
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
