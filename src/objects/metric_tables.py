from src.objects.data_objects import HTMLTableObject
from src.objects.metric_obj import *


class AllMetricsTable(HTMLTableObject):
    def build_dataframe(self):
        type_metrics_df = TypeMetricObj().data()

        return type_metrics_df\
            .merge(NumberOfCodeLinesMetricObj().data(), on='item', how='left') \
            .merge(NumberOfArgsInFunctionsMetricObj().data(), on='item', how='left') \
            .merge(IsScriptFile().data(), on='item', how='left')


if __name__ == '__main__':
    AllMetricsTable().data()
