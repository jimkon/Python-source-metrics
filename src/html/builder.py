import os.path
from abc import ABC

from src.configs import PATH_RES_HTML
from src.utils.io_files import read_text_from_file


class HTMLBuilder(ABC):
    def __init__(self, template_filename):
        self._html_str = read_text_from_file(os.path.join(PATH_RES_HTML, template_filename))

    def replace(self, this, with_that):
        self._html_str = self._html_str.replace(this, with_that)

    @property
    def html(self):
        return self._html_str


