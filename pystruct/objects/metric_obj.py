import ast

import matplotlib.pyplot as plt

from pystruct.utils.plots import plot_hist_and_quartiles

plt.style.use('bmh')

from pystruct.metrics.metrics_core import MetricObject
from pystruct.objects.data_objects import DataframeObjectABC, HTMLTableObjectABC
from pystruct.objects.metric_stats import ValueCountMetricObj, MatplotlibGraphMetricObj


class TypeMetricObj(MetricObject):
    def calculate(self, p_obj, **kwargs):
        return p_obj.type


class TypeMetricValueCountsTable(ValueCountMetricObj):
    def get_series(self):
        return TypeMetricObj().data()['type']


class NumberOfCodeLinesMetricObj(MetricObject):
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


class GeneralItemMetricObj(DataframeObjectABC):
    def build(self):
        df_lines = NumberOfCodeLinesMetricObj().data()
        df_types = TypeMetricObj().data()

        df = df_types.merge(df_lines, on='item', how='left')

        df_agg_stats = df.groupby('type').agg({
            'item': 'count',
            'number_of_lines': ['sum', 'min', 'mean', 'max']
        }).sort_values(by=[('item', 'count')]).reset_index()

        df_agg_stats.columns = df_agg_stats.columns.droplevel(0)

        df_agg_stats = df_agg_stats.rename(columns={
            '': 'type',
            'count': '# items',
            'sum': 'total # of lines',
            'min': 'min # of lines',
            'mean': 'mean # of lines',
            'max': 'max # of lines'
        })

        # df_agg_stats['total # of lines'] = df_agg_stats['total # of lines'].apply(lambda x: np.nan if x == np.nan else int(x))
        # df_agg_stats['min # of lines'] = df_agg_stats['min # of lines'].apply(lambda x: np.nan if x == np.nan else int(x))
        # df_agg_stats['max # of lines'] = df_agg_stats['max # of lines'].apply(lambda x: np.nan if x == np.nan else int(x))

        return df_agg_stats


class GeneralItemMetricHTMLTable(HTMLTableObjectABC):
    def build_dataframe(self):
        return GeneralItemMetricObj().data()


class NumberOfCodeLinesHistogram(MatplotlibGraphMetricObj):
    def build_plot(self):
        df_lines = NumberOfCodeLinesMetricObj().data()
        df_types = TypeMetricObj().data()
        df = df_types.merge(df_lines, on='item', how='left')

        plt.figure(figsize=(12, 5))

        for i, type in enumerate(['module', 'class', 'function', 'class_method']):
            plt.subplot(1, 4, i+1)
            plt.xlabel(type)
            if i == 0:
                plt.ylabel('number_of_lines')
            # plt.boxplot(df[df['type'] == type]['number_of_lines'])
            plot_hist_and_quartiles(df[df['type'] == type]['number_of_lines'])
        plt.tight_layout()


class NumberOfArgsInFunctionsMetricObj(MetricObject):
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


class FunctionArgsHistogram(MatplotlibGraphMetricObj):
    def build_plot(self):
        df_args = NumberOfArgsInFunctionsMetricObj().data()
        df_types = TypeMetricObj().data()
        df = df_types.merge(df_args, on='item', how='left')

        plt.figure(figsize=(8, 5))

        for i, type in enumerate(['function', 'class_method']):
            plt.subplot(1, 2, i + 1)
            plt.xlabel(type)
            if i == 0:
                plt.ylabel('number_of_args_in_functions')
            # plt.boxplot(df[df['type'] == type]['number_of_args_in_functions'])
            plot_hist_and_quartiles(df[df['type'] == type]['number_of_args_in_functions'])
        plt.tight_layout()


class IsScriptFile(MetricObject):
    metric_name = 'is_script_file'

    def calculate_module(self, module_obj, **kwargs):
        all_code = module_obj.code.replace('\n', '').replace(' ', '').replace('"', "'")
        return "if__name__=='__main__':" in all_code


