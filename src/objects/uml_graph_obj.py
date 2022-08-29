import json
import os
import tempfile

from src.configs import PATH_FILES_DIR
from src.html.image_html import HTMLImageBuilder
from src.html.pages.page import HTMLPage
from src.objects.data_objects import AbstractObject
from src.objects.python_object import PObject
from src.reports.uml_class import UMLClassBuilder
from src.utils.file_strategies import HTMLFile
from src.utils.uml_utils import produce_uml_diagram_from_text_file


class UMLClassDiagramObj(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def _uml_to_html(self, temp_dir, uml_doc):
        with open(os.path.join(temp_dir.name, "temp_uml_text_file.txt"), 'w') as temp_uml_text_file:
            temp_uml_text_file.write(uml_doc)
        outfile_name = f"{temp_uml_text_file.name}.png"
        produce_uml_diagram_from_text_file(temp_uml_text_file.name,
                                       output_path=outfile_name)
        return HTMLImageBuilder(outfile_name).html

    def build(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassBuilder()
        pobj.use_visitor(uml_builder)

        temp_dir = tempfile.TemporaryDirectory(dir=PATH_FILES_DIR, prefix="UMLClassDiagramObj_")
        html_page = HTMLPage()
        for doc in uml_builder.result():
            html = self._uml_to_html(temp_dir, doc)
            html_page.add(html)
        temp_dir.cleanup()

        return html_page.html


if __name__ == '__main__':
    UMLClassDiagramObj().data()
