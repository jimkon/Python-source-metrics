import base64
from PIL import Image
import os

from src.configs import PATH_RES_HTML_IMAGE
from src.html.builder import HTMLBuilder
from src.utils.storage_mixins import StoreHTMLImageBuilds


class HTMLImageBuilder(HTMLBuilder):
    def __init__(self, image_path):
        super(HTMLImageBuilder, self).__init__()
        self._image_path = image_path
        self.build()
        self.save()

    @property
    def image_path(self):
        return self._image_path

    def template_file(self):
        return PATH_RES_HTML_IMAGE

    def replace(self, this, with_that):
        self._html_str = self._html_str.replace(this, with_that)

    def build(self):
        self.add_image(self._image_path)

    def add_image(self, image_path, size=None):
        with open(image_path, "rb") as image_file:
            image_base64_str = base64.b64encode(image_file.read()).decode("utf-8")
        self.replace('[image]', image_base64_str)

        if not size:
            size = Image.open(image_path).size
        self.replace('[width]', str(size[0]))
        self.replace('[height]', str(size[1]))

        return self

    def filename(self):
        return f"{os.path.basename(self._image_path)}.html"


if __name__ == '__main__':
    # TODO [continue] na treksw ayto
    # t = HTMLImageBuilder(r"C:\Users\jim\PycharmProjects\Python-source-metrics\files\uml\class_uml.png")
    t = HTMLImageBuilder().add_image(r"C:\Users\jim\Desktop\download.gif")
    print(t.html())
    StoreHTMLImageBuilds(t).save()

