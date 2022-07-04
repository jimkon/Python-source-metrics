from src.configs import PATH_RES_HTML_TABS
from src.utils.io_files import read_text_from_file
from src.utils.storage_mixins import StoreText


class HTMLTabsPageBuilder(StoreText):
    def __init__(self):
        self._html_str = read_text_from_file(PATH_RES_HTML_TABS)
        self._add_default_id = True

        self.add_tab("example1", "<h1>example1 html</h1>")
        self.add_tab("example2", read_text_from_file(r"C:\Users\jim\PycharmProjects\Python-source-metrics\files\joint_stats.csv.html"))
        self.save()

    def _replace(self, this, with_that):
        self._html_str = self._html_str.replace(this, with_that)

    def add_button(self, label):
        default_id = "id=\"defaultOpen\"" if self._add_default_id else ""
        self._add_default_id = False
        to_add = f"<button class=\"tablinks\" onclick=\"openCity(event, '{label}')\" {default_id}>{label}</button>\n\t[button]"
        self._replace('[button]', to_add)

    def add_div(self, label, html_content):
        to_add = f"<div id=\"{label}\" class=\"tabcontent\">\n{html_content}\n</div>\n[div_tab]"
        self._replace('[div_tab]', to_add)

    def add_tab(self, label, html_content):
        self.add_button(label)
        self.add_div(label, html_content)

    def html(self):
        self._replace("[button]", '')
        self._replace("[div_tab]", '')
        return self._html_str

    def data_to_store(self):
        return self.html()

    def path_to_store(self):  # TODO
        return r"C:\Users\jim\PycharmProjects\Python-source-metrics\files\tabs.csv.html"


if __name__ == '__main__':
    t = HTMLTabsPageBuilder()
    print(t.html())

