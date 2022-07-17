import os.path
from abc import ABC, abstractmethod

from src.configs import PATH_RES_HTML
from src.utils.io_files import read_text_from_file
from src.utils.storage_mixins import StoreHTMLBuilds


class HTMLBuilder(StoreHTMLBuilds, ABC):
    def __init__(self):
        self._html_str = read_text_from_file(os.path.join(PATH_RES_HTML, self.template_file()))

    def replace(self, this, with_that):
        self._html_str = self._html_str.replace(this, with_that)

    @abstractmethod
    def build(self):
        pass

    def html(self):
        self.build()
        return self._html_str

    def data_to_store(self):
        return self.html()

    @abstractmethod
    def template_file(self):
        pass


