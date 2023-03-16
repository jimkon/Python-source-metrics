from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.objects.data_objects import AbstractObject
from pystruct.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages
from pystruct.objects.metric_tables import AllMetricsTable, AllMetricsStatsHTML
from pystruct.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, InProjectImportModuleGraphObj, \
    PackagesImportModuleGraphObj
from pystruct.utils.file_strategies import HTMLFile


class FullReport(AbstractObject):
    def __init__(self):
        super().__init__(HTMLFile(self))

    def build(self):
        html_builder = TabsHTML()
        html_builder.add_tab("General info", AllMetricsStatsHTML().data())
        html_builder.add_tab("UML Class diagram", UMLClassDiagramObj().data())
        html_builder.add_tab("UML Relation diagram", UMLClassRelationDiagramObj().data())
        html_builder.add_tab("Imports table", HTMLPage()
                             .add_element(MostImportedPackages().data())
                             .add_element(MostImportedProjectModules().data())
                             .add_element(MostImportedProjectPackages().data())
                             .add_element(UnusedModules().data())
                             .add_element(InvalidImports().data())
                             .html())


        html_builder.add_tab("In project Import graphs", InProjectImportModuleGraphObj().data())

        html_builder.add_tab("Package Import graphs", PackagesImportModuleGraphObj().data())

        html_builder.add_tab("Metrics table", HTMLPage()
                             .add_element(AllMetricsTable().data())
                             .html())

        return html_builder.html()


if __name__ == '__main__':
    FullReport().data()
