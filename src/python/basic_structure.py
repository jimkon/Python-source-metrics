import abc


# TODO project object can be a tree node subclass called head (no parent)
# TODO check if tree node get item can be chained example node['src']['utils']['ast_utils]['analyse_ast']
# TODO Init visitor can take argument ex. "functions" and expand only until functions (instead to all the way down to identifiers)
from functools import cached_property

from src.utils.ast_utils import analyse_ast, remove_first_n_characters


class Node:
    def __init__(self):
        self.__depth = 0

    def set_depth(self, depth):
        self.__depth = depth

    def get_depth(self):
        return self.__depth

    def accept(self, visitor):
        visitor.visit(self)


class TreeNode(abc.ABC, Node):
    def __init__(self, filename, parent=None):
        super().__init__()
        self.__filename = filename
        self.__branches = None
        self.__parent = parent

    @property
    def filename(self):
        return self.__filename

    @abc.abstractmethod
    def name(self):
        pass

    def set_branches(self, list_objs):
        if self.__branches is None:
            self.__branches = {}
            for obj in list_objs:
                obj.set_depth(self.get_depth()+1)
                self.__branches[obj.name] = obj

    @property
    def branches(self):
        return self.__branches

    @property
    def parent(self):
        return self.__parent

    def pre_order_visit(self, visitor):
        self.accept(visitor)
        if self.branches:
            for name, branch in self.branches.items():
                branch.pre_order_visit(visitor)

    def __getitem__(self, item):
        return self.branches[item]


class CodeObjMixin(abc.ABC):
    @abc.abstractmethod
    @cached_property
    def code(self):
        pass

    @cached_property
    def ast(self):
        return analyse_ast(self.code)

    @cached_property
    def code_lines(self):
        return self.code.split('\n')


class CompoundStatementCodeMixin(CodeObjMixin, abc.ABC):
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
