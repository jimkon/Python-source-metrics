from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.objects.data_objects import AbstractObject, HTMLObject
from pystruct.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages, ImportsStatsHTML
from pystruct.objects.metric_tables import AllMetricsTable, AllMetricsStatsHTML
from pystruct.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, InProjectImportModuleGraphObj, \
    PackagesImportModuleGraphObj


class FullReport(HTMLObject):
    content_dict = {
        "General info": AllMetricsStatsHTML,
        "UML Class diagram": UMLClassDiagramObj,
        "UML Relation diagram": UMLClassRelationDiagramObj,
        "Imports table": ImportsStatsHTML,
        "In project Import graphs": InProjectImportModuleGraphObj,
        "Package Import graphs": PackagesImportModuleGraphObj,
        "Metrics table": AllMetricsTable,
    }

    def build(self):
        html_builder = TabsHTML()
        for title, obj_class in FullReport.content_dict.items():
            html_builder.add_tab(title, obj_class().data())

        return html_builder.html()


if __name__ == '__main__':
    FullReport().data()
