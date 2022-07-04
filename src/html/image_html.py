import base64
from PIL import Image

from src.configs import PATH_RES_HTML_IMAGE
from src.utils.io_files import read_text_from_file
from src.utils.storage_mixins import StoreText


class HTMLImageBuilder(StoreText):
    def __init__(self):
        self._html_str = read_text_from_file(PATH_RES_HTML_IMAGE)
        # self.add_image(r"C:\Users\jim\Desktop\download.gif")
        self.add_image(r"C:\Users\jim\PycharmProjects\Python-source-metrics\files\uml\class_uml.png")

        self.save()

    def _replace(self, this, with_that):
        self._html_str = self._html_str.replace(this, with_that)
        print(self._html_str)

    def add_image(self, image_path, size=None):
        with open(image_path, "rb") as image_file:
            image_base64_str = base64.b64encode(image_file.read()).decode("utf-8")
        self._replace('[image]', image_base64_str)

        if not size:
            size = Image.open(image_path).size
        self._replace('[width]', str(size[0]))
        self._replace('[height]', str(size[1]))

    def html(self):

        return self._html_str

    def data_to_store(self):
        return self.html()

    def path_to_store(self):  # TODO
        return r"C:\Users\jim\PycharmProjects\Python-source-metrics\files\image.csv.html"


if __name__ == '__main__':
    t = HTMLImageBuilder()
    print(t.html())
