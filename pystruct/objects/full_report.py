from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.objects.data_objects import AbstractObject, HTMLObject
from pystruct.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages, ImportsStatsHTML
from pystruct.objects.metric_tables import AllMetricsTable, AllMetricsStatsHTML
from pystruct.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, InProjectImportModuleGraphObj, \
    PackagesImportModuleGraphObj


class FullReport(HTMLObject):
    def build(self):
        html_builder = TabsHTML()
        html_builder.add_tab("General info", AllMetricsStatsHTML().data())
        html_builder.add_tab("UML Class diagram", UMLClassDiagramObj().data())
        html_builder.add_tab("UML Relation diagram", UMLClassRelationDiagramObj().data())
        html_builder.add_tab("Imports table", ImportsStatsHTML().data())
        html_builder.add_tab("In project Import graphs", InProjectImportModuleGraphObj().data())

        html_builder.add_tab("Package Import graphs", PackagesImportModuleGraphObj().data())

        html_builder.add_tab("Metrics table", AllMetricsTable().data())

        return html_builder.html()


if __name__ == '__main__':
    FullReport().data()
