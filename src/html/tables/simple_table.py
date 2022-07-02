import pandas as pd


from src.configs import PATH_STORE_JOINT_STAT_TABLE_CSV, PATH_RES_HTML_TABLE
from src.utils.io_files import read_text_from_file
from src.utils.storage_mixins import StoreText

_table_template = read_text_from_file(PATH_RES_HTML_TABLE)


class HTMLTableBuilder:
    def __init__(self, title):
        self._html_str = _table_template
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
        self._replace('[rows]', '[row]\n    [rows]')
        cols_html = "".join([f"<td>{column}</td>" for column in row])
        cols_html = f"<tr>{cols_html}</tr>"
        self._replace('[row]', cols_html)

    def html(self):
        return self._html_str


class SimpleHTMLTable(StoreText):
    def __init__(self, csv_path):
        self._html_path = csv_path+".html"
        self._df = pd.read_csv(csv_path)

        self._html_builder = HTMLTableBuilder(csv_path)
        self._html_builder.add_column_names(self._df.columns)
        for row in self._df.iterrows():
            self._html_builder.add_row(row[1].values)

        self.save()

    def data_to_store(self):
        return self._html_builder.html()

    def path_to_store(self):
        return self._html_path


if __name__ == '__main__':
    SimpleHTMLTable(PATH_STORE_JOINT_STAT_TABLE_CSV)
