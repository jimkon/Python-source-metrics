import tempfile

import pandas as pd
import matplotlib.pyplot as plt

from src.html.image_html import HTMLImageBuilder

plt.style.use('bmh')

from src.html.pages.page import HTMLPage
from src.metrics.metric_sets import ALL_METRICS
from src.objects.data_objects import HTMLTableObject, DataframeObject, HTMLObject


class AllMetricsDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None}, to_csv_kwargs={'index': False})

    def build(self):
        df = ALL_METRICS[0]().data()

        for metric_obj in ALL_METRICS[1:]:
            df = df.merge(metric_obj().data(), on='item', how='left')

        return df


class AllMetricsTable(HTMLTableObject):
    def build_dataframe(self):
        return AllMetricsDataframe().data()


class AllMetricsStatsObj(HTMLObject):
    def build(self):
        page = HTMLPage()

        self._df_all_stats = AllMetricsDataframe().data()
        [page.add(stats_html) for stats_html in self.number_stats()]

    def number_stats(self):
        res = []

        df_numbers = self._df_all_stats.select_dtypes('number')
        for col in df_numbers.columns:
            df_metric = pd.concat([
                self._df_all_stats[['item']],
                df_numbers[[col]]],
                axis=1
            )

            res.append(_hist(df_metric))
            t = 1

        exit()
        return res


def _hist(df):
    x_col_name, y_col_name = df.columns[:2]

    plt.figure()
    plt.title(y_col_name)
    plt.hist(df[y_col_name], bins=50)
    # res_dict = plt.boxplot(df[y_col_name], showmeans=True)
    # print(res_dict)
    # print(res_dict['fliers'])
    # print(res_dict['fliers'][0].get_data())
    # print(dir(res_dict['fliers'][0].get_xdata()))
    plt.yscale('log')
    plt.grid()
    plt.show()
    return _plt_fig_to_image_html()


def _plt_fig_to_image_html():
    with tempfile.NamedTemporaryFile(suffix='_image.png') as tmp_file:
        plt.savefig(tmp_file.name)
        return HTMLImageBuilder(tmp_file.name).html


if __name__ == '__main__':
    AllMetricsStatsObj().data()
