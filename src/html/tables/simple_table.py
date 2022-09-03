import pandas as pd


from src.configs import PATH_STORE_JOINT_STAT_TABLE_CSV, PATH_RES_HTML_TABLE
from src.utils.io_files import read_text_from_file
from src.utils.storage_mixins import StoreText


class HTMLTableBuilder:
    def __init__(self, title):
        self._html_str = read_text_from_file(PATH_RES_HTML_TABLE)
        self.add_title(title)

    def _replace(self, this, with_that):
        self._html_str = self._html_str.replace(this, with_that)

    def add_title(self, title):
        self._replace('[title]', title)

    def add_column_names(self, columns):
        cols_html = "".join([f"<th>{column}</th>" for column in columns])
        cols_html = f"<tr>{cols_html}</tr>"
        self._replace('[columns]', cols_html)

    def add_row(self, row):
        cols_html = "".join([f"<td>{column}</td>" for column in row])
        cols_html = f"<tr>{cols_html}</tr>\n    [row]"
        self._replace('[row]', cols_html)

    def html(self):
        self._replace("[row]", '')
        return self._html_str


class SimpleHTMLTable:
    def __init__(self, df, title=''):
        self._df = df

        self._html_builder = HTMLTableBuilder(title)
        self._html_builder.add_column_names(self._df.columns)
        for row in self._df.iterrows():
            self._html_builder.add_row(row[1].values)

    @property
    def html(self):
        return self._html_builder.html()


# if __name__ == '__main__':
#     SimpleHTMLTableBuilder(PATH_STORE_JOINT_STAT_TABLE_CSV)
