from src.configs import PATH_STORE_FULL_REPORT_HTML
from src.html.page.mutli_tabs import HTMLTabsPageBuilder
from src.python.python_source_obj import PythonSourceObj
from src.utils.storage_mixins import StoreReports


class FullReport(StoreReports):

    _file = PATH_STORE_FULL_REPORT_HTML

    def __init__(self, python_source_obj):
        super(StoreReports, self).__init__(self._file)

        self._python_source_obj = python_source_obj
        self._html_builder = HTMLTabsPageBuilder()
        self._build_html()

        self.save()
        self.clear()

    def _build_html(self):
        pass

    def data_to_store(self):
        return self._html_builder.html()

    def clear(self):
        pass


if __name__ == '__main__':
    obj = PythonSourceObj("C:/Users/jim/PycharmProjects/Python-source-metrics/src")
    FullReport(obj)
