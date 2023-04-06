from pystruct.html_utils.html_pages import TabsHTML
from pystruct.objects.data_objects import HTMLObject
from pystruct.objects.imports_data_objects import ImportsStatsHTML
from pystruct.objects.metric_tables import AllMetricsTable, AllMetricsStatsHTML
from pystruct.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, \
    DependencyReportObj


class FullReport(HTMLObject):
    content_dict = {
        "General info": AllMetricsStatsHTML,
        "UML Class diagram": UMLClassDiagramObj,
        "UML Relation diagram": UMLClassRelationDiagramObj,
        "Imports table": ImportsStatsHTML,
        "Dependencies": DependencyReportObj,
        # "In project Import graphs": InProjectImportModuleGraphObj,
        # "Commercial Package Import graphs": PackagesImportModuleGraphObj,
        # "In-project Package Import graphs": HighLevelPackagesRelationsGraphObj,
        "Metrics table": AllMetricsTable,
    }

    def build(self):
        html_builder = TabsHTML()
        for title, obj_class in self.content_dict.items():
            html_builder.add_tab(title, obj_class().data())

        return html_builder.html()


if __name__ == '__main__':
    FullReport().data()
