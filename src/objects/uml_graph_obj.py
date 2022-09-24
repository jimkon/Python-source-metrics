from src.html.pages.page import HTMLPage
from src.objects.data_objects import AbstractObject
from src.objects.python_object import PObject
from src.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder
from src.utils.file_strategies import HTMLFile
from src.utils.plantuml_utils import produce_plantuml_diagrams_in_html_images_multithreading, produce_plantuml_diagrams_in_html_images


class UMLClassDiagramObj(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassBuilder()
        pobj.use_visitor(uml_builder)

        plantuml_doc_strings = uml_builder.result()

        plantuml_diagram_html_images = produce_plantuml_diagrams_in_html_images_multithreading(plantuml_doc_strings)

        html_page = HTMLPage()
        [html_page.add(html_image) for html_image in plantuml_diagram_html_images]

        return html_page.html


class UMLClassRelationDiagramObj(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassRelationBuilder()
        pobj.use_visitor(uml_builder)

        plantuml_doc_strings = [uml_builder.result()]

        plantuml_diagram_html_images = produce_plantuml_diagrams_in_html_images(plantuml_doc_strings)

        html_page = HTMLPage()
        [html_page.add(html_image) for html_image in plantuml_diagram_html_images]

        return html_page.html


if __name__ == '__main__':
    UMLClassDiagramObj().data()
    UMLClassRelationDiagramObj().data()
