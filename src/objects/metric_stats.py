import abc
import os
import tempfile

import pandas as pd
import matplotlib.pyplot as plt

from src.html.image_html import HTMLImageBuilder
from src.objects.data_objects import HTMLTableObject, HTMLObject


class ValueCountMetricObj(HTMLTableObject, abc.ABC):
    @abc.abstractmethod
    def get_series(self):
        pass

    def build_dataframe(self):
        series = self.get_series()
        res = pd.DataFrame(series.value_counts()).reset_index()
        return res


class MatplotlibGraphMetricObj(HTMLObject, abc.ABC):
    @abc.abstractmethod
    def build_plot(self):
        pass

    def build(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='_image.png', delete=False)
        self.build_plot()
        plt.savefig(tmp_file.name)

        res_image_html = HTMLImageBuilder(tmp_file.name).html

        tmp_file.close()
        os.unlink(tmp_file.name)

        return res_image_html


class HistoryGraphMetricObj(MatplotlibGraphMetricObj, abc.ABC):
    @abc.abstractmethod
    def get_df(self):
        pass

    def build_plot(self):
        plt.figure()
        self._hist(self.get_df())

    @staticmethod
    def _hist(df):
        x_col_name, y_col_name = df.columns[:2]

        plt.title(y_col_name)
        plt.hist(df[y_col_name], bins=50)
