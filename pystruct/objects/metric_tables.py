import matplotlib.pyplot as plt

from pystruct.objects.metric_obj import NumberOfCodeLinesHistogram, GeneralItemMetricHTMLTable, \
    FunctionArgsHistogram

plt.style.use('bmh')

from pystruct.html_utils.html_pages import HTMLPage
from pystruct.metrics.metric_sets import ALL_METRICS
from pystruct.objects.data_objects import HTMLTableObjectABC, DataframeObjectABC, HTMLObjectABC


class AllMetricsDataframe(DataframeObjectABC):
    def build(self):
        df = ALL_METRICS[0]().data()

        for metric_obj in ALL_METRICS[1:]:
            df = df.merge(metric_obj().data(), on='item', how='left')

        return df


class AllMetricsTable(HTMLTableObjectABC):
    def build_dataframe(self):
        return AllMetricsDataframe().data()


class AllMetricsStatsHTML(HTMLObjectABC):
    def build(self):
        page = HTMLPage()
        page.add_element(GeneralItemMetricHTMLTable().data())
        page.add_element(NumberOfCodeLinesHistogram().data())
        page.add_element(FunctionArgsHistogram().data())
        return page.html()


if __name__ == '__main__':
    AllMetricsStatsHTML().data()
