import pandas as pd
import markdown

from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.objects.data_objects import AbstractObject, HTMLObject, DataframeObject
from pystruct.objects.imports_data_objects import InProjectImportModuleGraphDataframe, \
    PackagesImportModuleGraphDataframe, ImportsEnrichedDataframe
from pystruct.objects.python_object import PObject
from pystruct.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder, ObjectRelationGraphBuilder, \
    PackageRelationGraphBuilder, PlantUMLPackagesAndModulesBuilder
from pystruct.utils.file_strategies import HTMLFile
from pystruct.utils.graph_structures import Graph
from pystruct.utils.plantuml_utils import PlantUMLService
from utils.color_utils import getDistinctColors


class PackageColorMappingDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None, 'header':0}, to_csv_kwargs={'index': False})

    def build(self):
        df = ImportsEnrichedDataframe().data()
        all_packages = sorted(list(set(df['package'].unique()).union(df['import_package'].dropna().unique())))
        package_colors = getDistinctColors(len(all_packages), luminance=.75, saturation=.5)
        res_df = pd.DataFrame({'package': all_packages, 'color': package_colors})
        return res_df



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


class PackageRelationsGraphObj(PlantUMLDiagramObj):

    def plantuml_docs(self):
        df = ImportsEnrichedDataframe().data()
        df_filtered = df[df['is_project_module']][['module', 'package', 'import_package']].drop_duplicates()
        df_agg = df_filtered.groupby(['package', 'import_package'], as_index=False).size()

        package_colors = {k: v['color'] for k, v in
                          PackageColorMappingDataframe().data().set_index('package').to_dict(orient='index').items()}

        total_imports_dict = {k: v['size'] for k, v in df_agg.groupby('package').agg({'size': 'sum'}).to_dict(orient='index').items()}
        times_imported_dict = {k: v['size'] for k, v in df_agg.groupby('import_package').agg({'size': 'sum'}).to_dict(orient='index').items()}

        df_agg['arrow_color'] = df_agg['import_package'].map(package_colors)

        plantuml_doc = PlantUMLPackagesAndModulesBuilder()
        for package, color in package_colors.items():
            total_imports = total_imports_dict.get(package, 0)
            times_imported = times_imported_dict.get(package, 0)

            plantuml_doc.start_container('object', package, color)
            plantuml_doc.add_note(f"imports: {total_imports}\nimported: {times_imported}")
            plantuml_doc.end_container()

        for package, import_package, size, arrow_color in df_agg.values.tolist():
            plantuml_doc.add_relation(package, '--|>', import_package, arrow_color, f":{size}")

        plantuml_doc_string = plantuml_doc.finish_and_return()
        return plantuml_doc_string


class PackageAndModuleRelationsGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = ImportsEnrichedDataframe().data()
        df = df[df['is_project_module'] & (~df['is_init_file'])]

        package_colors = {k: v['color'] for k, v in
                          PackageColorMappingDataframe().data().set_index('package').to_dict(orient='index').items()}
        df['arrow_color'] = df['import_package'].map(package_colors)

        plantuml_doc = PlantUMLPackagesAndModulesBuilder()

        for package, color in package_colors.items():
            modules = df[df['package'] == package]['module'].unique()

            plantuml_doc.start_container('package', package, '<<Folder>>', color)
            for module in modules:
                plantuml_doc.add_object('object', module)
            plantuml_doc.end_container()

        df_filtered = df[['module', 'import_module', 'arrow_color']].drop_duplicates()
        for module, import_module, arrow_color in df_filtered.values.tolist():
            plantuml_doc.add_relation(module, '<|--', import_module, arrow_color)

        plantuml_doc_string = plantuml_doc.finish_and_return()
        return plantuml_doc_string


class ModuleRelationGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = ImportsEnrichedDataframe().data()
        self._df = df[df['is_project_module']]
        modules, import_modules = self._df['module'].tolist(), self._df['import_module'].tolist()
        subgraphs = Graph(list(zip(modules, import_modules))).subgraphs()
        docs = [self.produce_doc_for_modules(subgraph.nodes) for subgraph in subgraphs]
        return docs

    def produce_doc_for_modules(self, modules):
        df = self._df[self._df['module'].isin(modules) | self._df['import_module'].isin(modules)]
        plantuml_doc = PlantUMLPackagesAndModulesBuilder(separator='set separator none')

        # TODO DictObjects for PackageColorMappingDataframe
        package_colors = {k: v['color'] for k, v in PackageColorMappingDataframe().data().set_index('package').to_dict(orient='index').items()}

        df_mods = pd.DataFrame(df[['module', 'package']].values.tolist()+df[['import_module', 'import_package']].values.tolist(),
                               columns=['module', 'package']).drop_duplicates()
        df_mods['color'] = df_mods['package'].map(package_colors)
        for module, package, color in df_mods.values.tolist():
            plantuml_doc.add_object('object', module, color)

        df['arrow_color'] = df['import_package'].map(package_colors)
        df = df[['module', 'import_module', 'arrow_color']].drop_duplicates()
        for module, import_module, arrow_color in df.values.tolist():
            plantuml_doc.add_relation(module, '<|--', import_module, arrow_color)

        plantuml_doc_string = plantuml_doc.finish_and_return()
        return plantuml_doc_string


class PackagesImportModuleGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = PackagesImportModuleGraphDataframe().data()

        plantuml_doc_strings = []
        for package in df['import_root'].unique():
            sub_df = df[df['import_root'] == package]
            module, import_root = sub_df['module'].tolist(), sub_df['import_root'].tolist()
            doc = ObjectRelationGraphBuilder(module, import_root).result()
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
        "Package Relations": PackageRelationsGraphObj,
        "Package-Module Relations": PackageAndModuleRelationsGraphObj,
        "Module relations": ModuleRelationGraphObj,
        "Commercial packages": PackagesImportModuleGraphObj,
    }

    def build(self):
        html_builder = TabsHTML()
        for title, obj_class in self.content_dict.items():
            html_builder.add_tab(title, obj_class().data())

        return html_builder.html()


if __name__ == '__main__':
    # DependencyAnalysisObj().data()
    # UMLClassDiagramObj().data()
    # UMLClassRelationDiagramObj().data()
    # ModuleRelationGraphObj().data()
    # PackageAndModuleRelationsGraphObj().data()
    PackageRelationsGraphObj().data()
    # PackagesImportModuleGraphObj().data()
