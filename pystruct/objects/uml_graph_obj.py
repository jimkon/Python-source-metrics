import pandas as pd
import markdown

from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.objects.data_objects import AbstractObject, HTMLObject
from pystruct.objects.imports_data_objects import InProjectImportModuleGraphDataframe, \
    PackagesImportModuleGraphDataframe, ImportsEnrichedDataframe
from pystruct.objects.python_object import PObject
from pystruct.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder, ObjectRelationGraphBuilder, \
    PackageRelationGraphBuilder
from pystruct.utils.file_strategies import HTMLFile
from pystruct.utils.graph_structures import Graph
from pystruct.utils.plantuml_utils import PlantUMLService


class PlantUMLDiagramObj(AbstractObject):
    def __init__(self, multithread=False):
        super().__init__(HTMLFile(self))
        self._plant_uml = PlantUMLService(multithread)

    def build(self):
        docs = self.plantuml_docs()

        if isinstance(docs, str):
            docs = [docs]

        plantuml_diagram_html_images = self._plant_uml.convert_multiple_docs_to_html_images(docs)

        html_page = HTMLPage()
        [html_page.add_element(html_image) for html_image in plantuml_diagram_html_images]

        return html_page.html()

    def plantuml_docs(self):
        pass


class UMLClassDiagramObj(PlantUMLDiagramObj):
    def __init__(self):
        super().__init__(multithread=True)

    def plantuml_docs(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassBuilder()
        pobj.use_visitor(uml_builder)

        plantuml_doc_strings = uml_builder.result()

        return plantuml_doc_strings


class UMLClassRelationDiagramObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassRelationBuilder()
        pobj.use_visitor(uml_builder)

        plantuml_doc_strings = uml_builder.result()

        plantuml_doc_strings = UMLClassRelationDiagramObj.split_documents(plantuml_doc_strings)
        return plantuml_doc_strings

    @staticmethod
    def split_documents(graph_doc):
        graph_doc_lines = graph_doc.split('\n')
        class_relations_lines = [line for line in graph_doc_lines if '<|--' in line]
        class_relations = [line.split(' <|-- ') for line in class_relations_lines]

        subgraphs = [graph.nodes for graph in Graph(class_relations).subgraphs()]

        subgraph_docs = []
        for subgraph in subgraphs:
            subgraph_lines = [line for line in graph_doc_lines if any([_class in line for _class in subgraph])]
            subgraph_doc = '@startuml\nleft to right direction\n'+'\n'.join(subgraph_lines)+'\n@enduml'

            subgraph_docs.append(subgraph_doc)

        return subgraph_docs


class InProjectImportModuleGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = InProjectImportModuleGraphDataframe().data()
        plantuml_doc_strings = ObjectRelationGraphBuilder(df.values.tolist()).result()
        return plantuml_doc_strings


class HighLevelPackagesRelationsGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = ImportsEnrichedDataframe().data()
        df_filtered = df[df['is_project_module']][['package', 'import_package']]
        df_agg = df_filtered.groupby(['package', 'import_package'], as_index=False).size()

        # TODO pkg_items is ready but cannot be printed
        # pkg_items = {k: v['module'] for k, v in df.groupby('package').agg({'module': set}).to_dict(orient='index').items()}
        pkg_items = None

        plantuml_doc_strings = PackageRelationGraphBuilder(
            df_agg['package'].tolist(),
            df_agg['import_package'].tolist(),
            df_agg['size'].tolist(),
            package_items=pkg_items,
        ).result()
        return plantuml_doc_strings


class PackagesImportModuleGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = PackagesImportModuleGraphDataframe().data()

        plantuml_doc_strings = []
        for package in df['import_root'].unique():
            doc = ObjectRelationGraphBuilder(df[df['import_root'] == package].values.tolist()).result()
            plantuml_doc_strings.append(doc)
        return plantuml_doc_strings


class DependencyAnalysisObj(HTMLObject):
    def build(self):
        df = ImportsEnrichedDataframe().data()
        df = df[(~df['is_no_imports']) & (~df['is_init_file'])]
        total_n_packages = df['package'].nunique()
        total_n_modules = df['module'].nunique()
        com_packages = df[~df['is_project_module']]['import_root'].unique()
        n_com_packages = len(com_packages)
        n_module_deps = df[df['is_project_module']].groupby('module').agg({'import_module': pd.Series.nunique})['import_module'].sum()
        n_package_deps = df[df['is_project_module']].groupby('package').agg({'import_package': pd.Series.nunique})['import_package'].sum()
        return markdown.markdown("""# Dependency analysis    
Total number of packages=**{total_n_packages}**, total number of modules=**{total_n_modules}**   
        Commercial packages used = (**{n_com_packages}**){com_packages}   
        # of module dependencies = **{n_module_deps}**, # of package dependencies = **{n_package_deps}**
        """.format(**locals()))


class DependencyReportObj(HTMLObject):
    content_dict = {
        'Analysis': DependencyAnalysisObj,
        "Package Relations (high level view)": HighLevelPackagesRelationsGraphObj,
        "Commercial packages": PackagesImportModuleGraphObj,
        "In project Import graphs": InProjectImportModuleGraphObj,
    }

    def build(self):
        html_builder = TabsHTML()
        for title, obj_class in self.content_dict.items():
            html_builder.add_tab(title, obj_class().data())

        return html_builder.html()


if __name__ == '__main__':
    DependencyAnalysisObj().data()
    # UMLClassDiagramObj().data()
    # UMLClassRelationDiagramObj().data()
    # InProjectImportModuleGraphObj().data()
    # HighLevelPackagesRelationsGraphObj().data()
    # PackagesImportModuleGraphObj().data()
