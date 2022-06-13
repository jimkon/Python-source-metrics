import ast

from src.python.basic_structure import PythonCodeObj
from src.metrics.metrics_core import Metric, TypeMetric


class NumberOfCodeLinesMetric(Metric):
    name = 'number_of_lines'

    def _calc(self, p_obj):
        return len(p_obj.code_lines)

    def calculate_module(self, module_obj, **kwargs):
        return self._calc(module_obj)

    def calculate_class(self, class_obj, **kwargs):
        return self._calc(class_obj)

    def calculate_function(self, function_obj, **kwargs):
        return self._calc(function_obj)


class NumberOfArgsInFunctionsMetric(Metric):
    name = 'number_of_args_in_functions'

    @staticmethod
    def _fetch_args(p_obj):
        args = [_ast.arg for _ast in p_obj.ast if isinstance(_ast, ast.arg)]
        return args

    def calculate_function(self, function_obj, **kwargs):
        args = NumberOfArgsInFunctionsMetric._fetch_args(function_obj)
        return len(args)

    def calculate_class_method(self, class_method_obj, **kwargs):
        args = set(NumberOfArgsInFunctionsMetric._fetch_args(class_method_obj))
        args.discard('self')
        args.discard('args')
        args.discard('kwargs')
        return len(args)
