from src.html.pages.multi_tabs import HTMLTabsPageBuilder
from src.html.pages.page import HTMLPage
from src.objects.data_objects import AbstractObject
from src.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages
from src.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj
from src.utils.file_strategies import HTMLFile


class FullReport(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        html_builder = HTMLTabsPageBuilder()
        html_builder.add_tab("UML Class diagram", UMLClassDiagramObj().data())
        html_builder.add_tab("UML Relation diagram", UMLClassRelationDiagramObj().data())
        html_builder.add_tab("Imports table", HTMLPage()
                             .add(MostImportedPackages().data())
                             .add(MostImportedProjectModules().data())
                             .add(MostImportedProjectPackages().data())
                             .add(UnusedModules().data())
                             .add(InvalidImports().data())
                             .html)

        return html_builder.html


if __name__ == '__main__':
    FullReport().data()
