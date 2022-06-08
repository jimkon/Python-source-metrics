import ast

from src.python.basic_structure import PythonCodeObj
from src.visitors.metrics_core import Metric


class NumberOfCodeLinesMetric(Metric):
    name = 'number_of_lines'

    def _calc(self, node):
        if not isinstance(node, PythonCodeObj):
            raise ValueError(f"Not a CodeObjMixin: {self}")

        return len(node.code_lines)

    def calculate_module(self, module_node, **kwargs):
        return self._calc(module_node)

    def calculate_class(self, class_node, **kwargs):
        return self._calc(class_node)

    def calculate_function(self, function_node, **kwargs):
        return self._calc(function_node)


class NumberOfArgsInFunctionsMetric(Metric):
    name = 'number_of_args_in_functions'

    @staticmethod
    def _fetch_args(node):
        args = [_ast.arg for _ast in node.ast if isinstance(_ast, ast.arg)]
        return args

    def calculate_function(self, node, **kwargs):
        args = NumberOfArgsInFunctionsMetric._fetch_args(node)
        return len(args)

    def calculate_class_method(self, node, **kwargs):
        args = set(NumberOfArgsInFunctionsMetric._fetch_args(node))
        args.discard('self')
        args.discard('args')
        args.discard('kwargs')
        return len(args)


