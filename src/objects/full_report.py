from src.html.pages.multi_tabs import HTMLTabsPageBuilder
from src.html.pages.page import HTMLPage
from src.objects.data_objects import AbstractObject
from src.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages
from src.objects.metric_tables import AllMetricsTable, AllMetricsStatsObj
from src.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, InProjectImportModuleGraphObj, \
    PackagesImportModuleGraphObj
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

        html_builder.add_tab("Metrics table", HTMLPage()
                             .add(AllMetricsTable().data())
                             .html)

        html_builder.add_tab("Metrics stats", AllMetricsStatsObj().data())

        html_builder.add_tab("In project Import graphs", InProjectImportModuleGraphObj().data())

        html_builder.add_tab("Package Import graphs", PackagesImportModuleGraphObj().data())

        return html_builder.html


if __name__ == '__main__':
    FullReport().data()
