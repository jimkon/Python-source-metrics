import ast

from src.metrics.metrics_core import MetricObject


class TypeMetricObj(MetricObject):
    name = 'type'

    def calculate(self, p_obj, **kwargs):
        return p_obj.type


class NumberOfCodeLinesMetricObj(MetricObject):
    name = 'number_of_lines'

    def _calc(self, p_obj):
        return len(p_obj.code_lines)

    def calculate_module(self, module_obj, **kwargs):
        return self._calc(module_obj)

    def calculate_class(self, class_obj, **kwargs):
        return self._calc(class_obj)

    def calculate_function(self, function_obj, **kwargs):
        return self._calc(function_obj)

    def calculate_class_method(self, function_obj, **kwargs):
        return self._calc(function_obj)


class NumberOfArgsInFunctionsMetricObj(MetricObject):
    name = 'number_of_args_in_functions'

    @staticmethod
    def _fetch_args(p_obj):
        args = [_ast.arg for _ast in p_obj.ast if isinstance(_ast, ast.arg)]
        return args

    def calculate_function(self, function_obj, **kwargs):
        args = self._fetch_args(function_obj)
        return len(args)

    def calculate_class_method(self, class_method_obj, **kwargs):
        args = set(self._fetch_args(class_method_obj))
        args.discard('self')
        args.discard('args')
        args.discard('kwargs')
        return len(args)


class IsScriptFile(MetricObject):
    name = 'is_script_file'

    def calculate_module(self, module_obj, **kwargs):
        all_code = module_obj.code.replace('\n', '').replace(' ', '').replace('"', "'")
        return "if__name__=='__main__':" in all_code


