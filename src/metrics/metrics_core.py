import abc
import os.path

import pandas as pd

from src.configs import PATH_STORE_METRIC_RESULTS
from src.utils.logs import log_yellow
from src.utils.storage_mixins import StoreCSV
from src.visitors.visitor import TreeNodeVisitor

"""
To add a new metric:
   * sub-class Metric class
   * implement any of the calculate_[obj] functions needed
"""


class CalculateMetricVisitor(TreeNodeVisitor, StoreCSV):
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

    @property
    def results(self):
        return self._results

    def path_to_store(self):
        return os.path.join(PATH_STORE_METRIC_RESULTS, self._metric.name+'.csv')

    def data_to_store(self):
        results_t = {
            'name': self.results.keys(),
            'value': self.results.values()
        }
        df = pd.DataFrame(results_t)
        return df

    def done(self):
        self.save()


class Metric(abc.ABC):
    name = 'no-name'

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


class TypeMetric(Metric):
    name = 'type'
    def calculate(self, p_obj, **kwargs):
        return p_obj.type
