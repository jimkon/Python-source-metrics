import os
from functools import cached_property

import pandas as pd

from src.python.python_obj_factory import ObjectFactory
from src.utils.path_utils import load_file_as_string
from src.utils.paths import Path
from src.visitors.init_visitor import PythonObjInitializer
from src.visitors.metrics_core import CalculateMetricPythonObjVisitor
from src.visitors.visitor import PrintPythonObjVisitor, VisitedMixin


class PythonSourceObj(VisitedMixin):
    def __init__(self, abspath):
        self._abspath = Path(abspath)
        self._obj_factory = ObjectFactory(self._abspath)
        if self._obj_factory.root_path.is_directory:
            self._head = self._obj_factory.directory(self._abspath.dotted_relpath)
        else:
            code = load_file_as_string(self._abspath.abspath)
            self._head = self._obj_factory.module(self._abspath.dotted_relpath, code)
        self._init_objs()

    def _init_objs(self):
        visitor = PythonObjInitializer(self._obj_factory)
        self._head.pre_order_visit(visitor)

    def print_objects(self):
        self.use_visitor(PrintPythonObjVisitor())

    def calculate_metric(self, metric):
        metric_visitor = CalculateMetricPythonObjVisitor(metric)
        self._head.pre_order_visit(metric_visitor)
        return pd.DataFrame.from_dict(metric_visitor.results, orient='index')

    def use_visitor(self, visitor):
        self._head.pre_order_visit(visitor)

    def _node(self):
        return self._head

