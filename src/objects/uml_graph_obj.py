import json
import os
import tempfile

from src.configs import PATH_FILES_DIR
from src.html.image_html import HTMLImageBuilder
from src.objects.data_objects import AbstractObject
from src.objects.python_object import PObject
from src.reports.uml_class import UMLClassBuilder
from src.utils.file_strategies import HTMLFile
from src.utils.uml_utils import produce_uml_diagram_from_text_file


class UMLClassDiagramObj(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassBuilder()
        pobj.use_visitor(uml_builder)

        temp_dir = tempfile.TemporaryDirectory(dir=PATH_FILES_DIR, prefix="UMLClassDiagramObj_")

        with open(os.path.join(temp_dir.name, "temp_uml_text_file.txt"), 'w') as temp_uml_text_file:
            uml_str = uml_builder.result()
            temp_uml_text_file.write(uml_str)
            print(temp_uml_text_file.name)

        temp_uml_img_file_path = os.path.join(temp_dir.name, "temp_uml_img_file.png")
        produce_uml_diagram_from_text_file(temp_uml_text_file.name, output_path=temp_uml_img_file_path)

        html_image = HTMLImageBuilder(temp_uml_img_file_path)
        temp_dir.cleanup()

        return html_image.html


if __name__ == '__main__':
    UMLClassDiagramObj().data()
