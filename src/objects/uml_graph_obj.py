import json
import os
import tempfile
import threading

from src.configs import PATH_FILES_DIR
from src.html.image_html import HTMLImageBuilder
from src.html.pages.page import HTMLPage
from src.objects.data_objects import AbstractObject
from src.objects.python_object import PObject
from src.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder
from src.utils.file_strategies import HTMLFile
from src.utils.logs import log_pink
from src.utils.uml_utils import produce_uml_diagram_from_text_file


def _uml_to_html(temp_dir, uml_doc):
    temp_file = tempfile.NamedTemporaryFile(suffix="_temp_uml_text_file.txt", dir=temp_dir.name, delete=False)
    with open(temp_file.name, 'w') as f:
        f.write(uml_doc)

    infile_name, outfile_name = temp_file.name, f"{temp_file.name}.png"
    produce_uml_diagram_from_text_file(infile_name,
                                       output_path=outfile_name)
    return HTMLImageBuilder(outfile_name).html


class UMLImageThread(threading.Thread):
    def __init__(self, temp_dir, uml_doc):
        threading.Thread.__init__(self)
        self._dir = temp_dir
        self._uml_doc = uml_doc
        self._result = None

    def run(self):
        import random
        id = random.randint(0, 1000)
        log_pink(f'Thread {id} started')
        self._result = _uml_to_html(self._dir, self._uml_doc)
        log_pink(f'-Thread {id} finished')

    def result(self):
        return self._result


class UMLClassDiagramObj(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassBuilder()
        pobj.use_visitor(uml_builder)

        temp_dir = tempfile.TemporaryDirectory(dir=PATH_FILES_DIR, prefix="UMLClassDiagramObj_")
        html_page = HTMLPage()

        # ******* MULTITHREADING SOLUTION *******
        threads = []
        for doc in uml_builder.result():
            thread = UMLImageThread(temp_dir, doc)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        [html_page.add(thread.result()) for thread in threads]
        # ***************************************

        # ******* SEQUENTIAL EXECUTION *******
        # for doc in uml_builder.result():
        #     html = _uml_to_html(temp_dir, doc)
        #     html_page.add(html)
        # ************************************

        temp_dir.cleanup()

        return html_page.html


class UMLClassRelationDiagramObj(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassRelationBuilder()
        pobj.use_visitor(uml_builder)

        temp_dir = tempfile.TemporaryDirectory(dir=PATH_FILES_DIR, prefix="UMLClassRelationDiagramObj_")
        html_page = HTMLPage()
        html = _uml_to_html(temp_dir, uml_builder.result())
        html_page.add(html)
        temp_dir.cleanup()

        return html_page.html


if __name__ == '__main__':
    UMLClassDiagramObj().data()
    UMLClassRelationDiagramObj().data()
