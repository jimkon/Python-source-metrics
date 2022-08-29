from src.html.pages.mutli_tabs import HTMLTabsPageBuilder
from src.objects.data_objects import AbstractObject
from src.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj
from src.utils.file_strategies import HTMLFile


class FullReport(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        html_builder = HTMLTabsPageBuilder()
        html_builder.add_tab("UML Class diagram", UMLClassDiagramObj().data())
        html_builder.add_tab("UML Relation diagram", UMLClassRelationDiagramObj().data())

        return html_builder.html


if __name__ == '__main__':
    FullReport().data()
