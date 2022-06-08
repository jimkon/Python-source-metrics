import abc

from src.visitors.visitor import PythonObjVisitor

"""
To add a new metric:
   * sub-class Metric class
   * implement any of the calculate_[obj] functions needed
"""


class CalculateMetricPythonObjVisitor(PythonObjVisitor):
    def __init__(self, metric):
        self._metric = metric
        self._results = {}

    def _set_value_for_node(self, node, value):
        if value is None:
            return False

        # [node.name] = value
        self._results[node.name] = value

        # [node.type][node.name] = value
        # if node.type not in self._results.keys() or self._results[node.type] is None:
        #     self._results[node.type] = {node.name: value}
        # else:
        #     self._results[node.type][node.name] = value

        return True

    def visit_all(self, node):
        self._set_value_for_node(node, self._metric.calculate(node))

    def visit_directory(self, node):
        self._set_value_for_node(node, self._metric.calculate_directory(node))

    def visit_module(self, node):
        self._set_value_for_node(node, self._metric.calculate_module(node))

    def visit_class(self, node):
        self._set_value_for_node(node, self._metric.calculate_class(node))

    def visit_function(self, node):
        self._set_value_for_node(node, self._metric.calculate_function(node))

    def visit_class_method(self, node):
        self._set_value_for_node(node, self._metric.calculate_class_method(node))

    @property
    def results(self):
        return self._results


class Metric(abc.ABC):
    def calculate(self, node, **kwargs):
        pass

    def calculate_directory(self, node, **kwargs):
        pass

    def calculate_module(self, node, **kwargs):
        pass

    def calculate_class(self, node, **kwargs):
        pass

    def calculate_function(self, node, **kwargs):
        pass

    def calculate_class_method(self, node, **kwargs):
        pass
