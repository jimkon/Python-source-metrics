import abc

import pandas as pd

from pystruct.objects.data_objects import DataframeObjectABC
from pystruct.objects.python_object import PObject
from pystruct.utils.logs import log_yellow
from pystruct.visitors.visitor import TreeNodeVisitor

"""
To add a new metric:
   * sub-class Metric class
   * implement any of the calculate_[obj] functions needed
"""


class CalculateMetricVisitor(TreeNodeVisitor):
    def __init__(self, metric):
        self._metric = metric
        self._results = {}

    def _set_value_for_obj(self, p_obj, value):
        if value is None:
            return False

        if p_obj.name in self._results.keys():
            log_yellow(f"Multiple values for metric {self._metric.name} (current value {self._results[p_obj.name]} overwritten with {value}.)")

        self._results[p_obj.name] = value
        return True

    def visit_all(self, node):
        self._set_value_for_obj(node.data, self._metric.calculate(node.data))

    def visit_directory(self, node):
        self._set_value_for_obj(node.data, self._metric.calculate_directory(node.data))

    def visit_module(self, node):
        self._set_value_for_obj(node.data, self._metric.calculate_module(node.data))

    def visit_class(self, node):
        self._set_value_for_obj(node.data, self._metric.calculate_class(node.data))

    def visit_function(self, node):
        self._set_value_for_obj(node.data, self._metric.calculate_function(node.data))

    def visit_class_method(self, node):
        self._set_value_for_obj(node.data, self._metric.calculate_class_method(node.data))

    def results(self):
        data_array = list(self._results.items())
        return pd.DataFrame.from_records(data_array, columns=['item', self._metric.metric_name])


class Metric(abc.ABC):
    metric_name = None

    def calculate(self, p_obj, **kwargs):
        pass

    def calculate_directory(self, p_obj, **kwargs):
        pass

    def calculate_module(self, p_obj, **kwargs):
        pass

    def calculate_class(self, p_obj, **kwargs):
        pass

    def calculate_function(self, p_obj, **kwargs):
        pass

    def calculate_class_method(self, p_obj, **kwargs):
        pass


class MetricObject(DataframeObjectABC, Metric):
    def __init__(self):
        super().__init__()

    def build(self):
        pobj = PObject().python_source_object()
        metrics_vis = CalculateMetricVisitor(self)
        pobj.use_visitor(metrics_vis)
        res = metrics_vis.results()
        return res
