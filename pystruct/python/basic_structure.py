import abc
# TODO project object can be a tree node subclass called head (no parent)
# TODO check if tree node get item can be chained example node['pystruct']['utils']['ast_utils]['analyse_ast']
# TODO Init visitor can take argument ex. "functions" and expand only until functions (instead to all the way down to identifiers)
from functools import cached_property

from pystruct.utils.ast_utils import analyse_ast, remove_first_n_characters
from pystruct.visitors.visitor import VisitedMixin


class NodeDepthAlreadySet(ValueError):
    pass


class NodeBranchesAlreadySet(ValueError):
    pass


class Node(VisitedMixin):
    def __init__(self, data, depth=-1):
        self.__data = data
        self.__depth = depth

    @property
    def data(self):
        return self.__data

    @property
    def depth(self):
        return self.__depth

    def set_depth(self, depth):
        if self.depth > -1:
            self.__depth = depth
        else:
            raise NodeDepthAlreadySet


class TreeNode(Node):
    def __init__(self, parent, data):
        super().__init__(data, parent.depth+1 if parent else 0)
        self.__branches = None
        self.__parent = parent

    def set_branches(self, list_objs):
        if self.__branches is None:
            self.__branches = {}
            for obj in list_objs:
                obj.set_depth(self.depth+1)
                self.__branches[obj.data.name] = obj
        else:
            raise NodeBranchesAlreadySet

    @property
    def branches(self):
        return self.__branches if self.__branches else {}

    @property
    def parent(self):
        return self.__parent

    def pre_order_visit(self, visitor):
        self.accept(visitor)
        if self.branches:
            for name, branch in self.branches.items():
                branch.pre_order_visit(visitor)

    def __str__(self):
        return f"(Node) {self.data}"

    # def __getitem__(self, item):
    #     return self.branches[item]


class PythonObjData(abc.ABC):
    type = None

    def __init__(self, name, path):
        self.__path = path
        self.__name = name

    @property
    def path(self):
        return self.__path

    @property
    def name(self):
        return self.__name

    @property
    def name_short(self):
        return self.name.split('.')[-1]

    def __str__(self):
        return f"{self.name}: {self.type.capitalize()}"


class PythonCodeObj(PythonObjData):
    def __init__(self, name, path, code):
        super().__init__(name, path)
        self.__code = code

    @property
    def code(self):
        return self.__code

    @cached_property
    def ast(self):
        return analyse_ast(self.code)

    @cached_property
    def code_lines(self):
        return self.code.split('\n')

    def __str__(self):
        return f"{super().__str__()}, code \"{self.code_lines[0]}\"..."


class CompoundStatementCodeMixin(PythonCodeObj):
    @cached_property
    def statement_def_ast(self):
        return self.ast[1]

    @cached_property
    def statement_def_lineno(self):
        return self.statement_def_ast.lineno

    @cached_property
    def statement_def(self):
        return self.code_lines[self.statement_def_lineno-1]

    @cached_property
    def statement_inner_code(self):
        inner_code_lines = self.code_lines[self.statement_def_lineno:]
        return '\n'.join(remove_first_n_characters(inner_code_lines, self.statement_def_ast.body[0].col_offset))

    @cached_property
    def statement_name(self):
        return self.statement_def_ast.name
