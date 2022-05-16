import os
from functools import cached_property

from src.python.python_obj_factory import ObjectFactory
from src.visitors.visitor import InitVisitor, PrintVisitor


class PythonSourceObj:
    def __init__(self, abspath):
        self._abspath = os.path.normpath(abspath)
        self._obj_factory = ObjectFactory(self._abspath)
        if os.path.isdir(self._abspath):
            self._head = self._obj_factory.directory(self.root_path)
        else:
            raise NotImplementedError
        self._init_objs()

    def _init_objs(self):
        visitor = InitVisitor(self._obj_factory)
        self._head.pre_order_visit(visitor)

    @cached_property
    def root_path(self):
        return os.path.basename(self._abspath)

    def print_objects(self):
        self._head.pre_order_visit(PrintVisitor())

