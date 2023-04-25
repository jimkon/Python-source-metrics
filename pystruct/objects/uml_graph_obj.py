import markdown
import pandas as pd

from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.metrics.import_metrics import breakdown_import_path
from pystruct.objects.data_objects import AbstractObject, HTMLObject, DataframeObject
from pystruct.objects.dependencies import PackageDependencyStatsDataframe, ModuleDependencyStatsDataframe, \
    PackageAndModulesMapping
from pystruct.objects.imports_data_objects import PackagesImportModuleGraphDataframe, ImportsEnrichedDataframe
from pystruct.objects.python_object import PObject
from pystruct.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder, ObjectRelationGraphBuilder, \
    PlantUMLPackagesAndModulesBuilder
from pystruct.utils.color_utils import getDistinctColors
from pystruct.utils.mixins import JSONableMixin
from pystruct.utils.file_strategies import HTMLFile
from pystruct.utils.graph_structures import Graph
from pystruct.utils.plantuml_utils import PlantUMLService


class PackageColorMappingDataframe(DataframeObject, JSONableMixin):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None, 'header':0}, to_csv_kwargs={'index': False})

    def build(self):
        df = ImportsEnrichedDataframe().data()
        all_packages = sorted(list(set(df['package'].unique()).union(df[df['is_internal']]['import_package'].dropna().unique())))
        package_colors = getDistinctColors(len(all_packages), luminance=.75, saturation=1.)
        vlight = getDistinctColors(len(all_packages), luminance=.75, saturation=.125)
        light = getDistinctColors(len(all_packages), luminance=.75, saturation=.25)
        medium = getDistinctColors(len(all_packages), luminance=.75, saturation=.5)
        strong = getDistinctColors(len(all_packages), luminance=.75, saturation=.75)
        vstrong = getDistinctColors(len(all_packages), luminance=.75, saturation=.875)
        res_df = pd.DataFrame({
            'package': all_packages,
            'color': package_colors,
            'very_light': vlight,
            'light': light,
            'medium': medium,
            'strong': strong,
            'very_strong': vstrong
        })
        return res_df

    def to_json(self):
        return self.data().set_index('package').to_dict(orient='index')


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
        df_pkgs = self.produce_data()

        plantuml_doc = PlantUMLPackagesAndModulesBuilder(direction='top to bottom direction')
        for row in df_pkgs.drop_duplicates(subset='package').iterrows():
            row = row[1]

            package = row['package']
            color = row['light']
            plantuml_doc.start_container('object', package, color)

            total_internal_imports = int(row['total_imports']) if row['total_imports'] else 0
            total_unique_internal_imports = int(row['number_of_internal_packages']) if row['number_of_internal_packages'] else 0
            internal_imports = self._present_packages(row['internal_packages'], remove_package_root=True) if row['internal_packages'] else ''
            total_external_imports = int(row['number_of_external_packages']) if row['number_of_external_packages'] else 0
            external_imports = self._present_packages(row['external_packages']) if row['external_packages'] else ''
            total_python_builtins = int(row['number_of_builtin_packages']) if row['number_of_builtin_packages'] else 0
            python_builtins = self._present_packages(row['builtin_packages']) if row['builtin_packages'] else ''
            total_imported = int(row['total_imported']) if row['total_imported'] else 0
            total_unique_imported = int(row['times_been_imported_from_packages']) if row['times_been_imported_from_packages'] else 0
            imported_from = self._present_packages(row['imported_from_packages'], remove_package_root=True) if row['imported_from_packages'] else ''
            plantuml_doc.add_note(  # TODO keep only package name on internals, not full package path
                f"IMPORTS\n"
                f"Internal: {total_internal_imports}  ({total_unique_internal_imports} unique)\n"
                f"> {internal_imports})\n"
                f"Python built-in: {total_python_builtins}\n"
                f"> {python_builtins}\n"
                f"Other: {total_external_imports}\n"
                f"> {external_imports}\n"
                f"Imported by: {total_imported}    ({total_unique_imported} unique)\n"
                f"> {imported_from}"
            )
            plantuml_doc.end_container()

        package_colors_dict = PackageColorMappingDataframe().to_json()
        for row in df_pkgs[(df_pkgs['import_package'] != False)].drop_duplicates(subset=['package', 'import_package']).iterrows():
            row = row[1]
            package = row['package']
            import_package = row['import_package']
            arrow_color = package_colors_dict[import_package]['color']
            num = int(row['size'])
            plantuml_doc.add_relation(package, '<|-[thickness=2]-', import_package, arrow_color, f":{num}")

        plantuml_doc_string = plantuml_doc.finish_and_return()
        return plantuml_doc_string

    def produce_data(self):
        df = ImportsEnrichedDataframe().data()
        df_filtered = df[df['is_internal']][['module', 'package', 'import_package']].drop_duplicates()
        df_agg = df_filtered.groupby(['package', 'import_package'], as_index=False).size()
        df_stats = PackageDependencyStatsDataframe().data()
        df_pkgs_colors = PackageColorMappingDataframe().data()

        total_imports_dict = {k: v['size'] for k, v in
                              df_agg.groupby('package').agg({'size': 'sum'}).to_dict(orient='index').items()}
        times_imported_dict = {k: v['size'] for k, v in
                               df_agg.groupby('import_package').agg({'size': 'sum'}).to_dict(orient='index').items()}

        df_pkgs = df_stats.merge(df[['package']].drop_duplicates(), on='package', how='left').\
            merge(df_pkgs_colors, on='package', how='left').\
            merge(df_agg, on='package', how='left')
        df_pkgs['total_imports'] = df_pkgs['package'].map(total_imports_dict)
        df_pkgs['total_imported'] = df_pkgs['package'].map(times_imported_dict)

        df_pkgs = df_pkgs.fillna(value=False)
        return df_pkgs

    @staticmethod
    def _present_packages(packages_str, remove_package_root=False):
        packages = packages_str.split(',')
        if remove_package_root:
            packages = PackageRelationsGraphObj._keep_package_names(packages)
        packages_sorted = sorted(packages)
        result_str = PackageRelationsGraphObj._create_multiline_string(packages_sorted)
        print(result_str)
        return result_str

    @staticmethod
    def _keep_package_names(packages):
        transform_func = lambda x: breakdown_import_path(x)[-1]
        packages_names = [transform_func(package) for package in packages]
        return packages_names

    @staticmethod
    def _create_multiline_string(strings, max_length=30, seperator=', '):
        """ ChatGPT
        Takes in a list of strings and concatenates them into a multiline string with a maximum line length
        specified by `max_length`. The `seperator` parameter is used to separate the individual strings in the
        concatenated string.

        Args:
            strings (list): A list of strings to concatenate into a multiline string.
            max_length (int): The maximum length of each line in the multiline string. Defaults to 30.
            seperator (str): The string to use to separate each string in the concatenated string. Defaults to ", ".

        Returns:
            str: The concatenated multiline string.

        Example:
            >>> strings = ["This", " is a long string", "This is another long string", "Yet another long string"]
            >>> _create_multiline_string(strings, max_length=20, seperator='; ')
            'This is a long string; \n> This is another long string; \n> Yet another long string'

        def test_create_multiline_string():
            # Test case 1: Strings fit within maximum line length
            strings = ["This is a long string", "This is another long string", "Yet another long string"]
            expected_output = "This is a long string, This is another long string, Yet another long string"
            assert _create_multiline_string(strings, max_length=30, seperator=', ') == expected_output

            # Test case 2: Strings need to be split into multiple lines
            strings = ["This is a long string", "This is another long string", "Yet another long string"]
            expected_output = "This is a long string,\n> This is another long string,\n> Yet another long string"
            assert _create_multiline_string(strings, max_length=20, seperator=', ') == expected_output

            # Test case 3: Empty list of strings
            strings = []
            expected_output = ""
            assert _create_multiline_string(strings, max_length=30, seperator=', ') == expected_output

            # Test case 4: Single string that is longer than max line length
            strings = ["This is a very long string that exceeds the maximum line length"]
            expected_output = "This is a very long string that exceeds the maximum line length"
            assert _create_multiline_string(strings, max_length=20, seperator=', ') == expected_output

            # Test case 5: Custom separator
            strings = ["This is a long string", "This is another long string", "Yet another long string"]
            expected_output = "This is a long string; \n> This is another long string; \n> Yet another long string"
            assert _create_multiline_string(strings, max_length=20, seperator='; ') == expected_output
        """
        output = ''
        current_line_length = 0

        for s in strings:
            if current_line_length + len(s) <= max_length:
                output += (seperator if len(output) > 0 else '')+s
                current_line_length += len(s)
            else:
                output += ',\n> ' + s
                current_line_length = len(s)

        return output



class PackageAndModuleRelationsGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df_pkgs, df_rels = self.produce_data()

        plantuml_doc = PlantUMLPackagesAndModulesBuilder()

        for package, color, modules in df_pkgs.values.tolist():
            plantuml_doc.start_container('package', package, '<<Folder>>', color)
            for module in modules:
                plantuml_doc.add_object('object', module)
            plantuml_doc.end_container()

        df_filtered = df_rels[~df_rels['import_module'].isna()][['module', 'import_module', 'very_strong']].drop_duplicates()
        for module, import_module, arrow_color in df_filtered.values.tolist():
            plantuml_doc.add_relation(module, '<|-[thickness=3]-', import_module, arrow_color)

        plantuml_doc_string = plantuml_doc.finish_and_return()
        return plantuml_doc_string

    def produce_data(self):
        df_pkgs_colors = PackageColorMappingDataframe().data()
        df_mods_and_pkgs = PackageAndModulesMapping().data()
        df_agg = df_mods_and_pkgs\
            .merge(df_pkgs_colors, on='package')\
            .groupby('package')\
            .agg({'light': 'first', 'module': pd.Series.unique})\
            .reset_index()

        df = ImportsEnrichedDataframe().data()
        df_filtered = df[df['is_internal'] & (~df['is_init_file'])]
        df_pkgs_colors = PackageColorMappingDataframe().data()
        df_stats = ModuleDependencyStatsDataframe().data()

        df_relations = df_stats.merge(df_filtered, on='module', how='left').merge(df_pkgs_colors, on='package', how='left')

        return df_agg, df_relations

class ModuleRelationGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = ImportsEnrichedDataframe().data()
        self._df = df[df['is_internal']]
        modules, import_modules = self._df['module'].tolist(), self._df['import_module'].tolist()
        subgraphs = Graph(list(zip(modules, import_modules))).subgraphs()
        docs = [self.produce_doc_for_modules(subgraph.nodes) for subgraph in subgraphs]
        return docs

    def produce_doc_for_modules(self, modules):
        df = self._df[self._df['module'].isin(modules) | self._df['import_module'].isin(modules)]
        plantuml_doc = PlantUMLPackagesAndModulesBuilder(direction='top to bottom direction', separator='set separator none')

        # TODO DictObjects for PackageColorMappingDataframe
        package_colors = {k: v['color'] for k, v in PackageColorMappingDataframe().data().set_index('package').to_dict(orient='index').items()}

        df_mods = pd.DataFrame(df[['module', 'package']].values.tolist()+df[df['is_internal']][['import_module', 'import_package']].values.tolist(),
                               columns=['module', 'package']).drop_duplicates()
        df_mods['color'] = df_mods['package'].map(package_colors)
        for module, package, color in df_mods.values.tolist():
            plantuml_doc.add_object('object', module, color)

        df['arrow_color'] = df[df['is_internal']]['import_package'].map(package_colors)
        df = df[['module', 'import_module', 'arrow_color']].drop_duplicates()
        for module, import_module, arrow_color in df.values.tolist():
            plantuml_doc.add_relation(module, '<|-[thickness=2]-', import_module, arrow_color)

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
        com_packages = df[~df['is_internal']]['import_root'].unique()
        n_com_packages = len(com_packages)
        n_module_deps = df[df['is_internal']].groupby('module').agg({'import_module': pd.Series.nunique})['import_module'].sum()
        n_package_deps = df[df['is_internal']].groupby('package').agg({'import_package': pd.Series.nunique})['import_package'].sum()
        markdown_to_html = markdown.markdown("""# Dependency analysis    
Total number of packages=**{total_n_packages}**, total number of modules=**{total_n_modules}**   
        Commercial packages used = (**{n_com_packages}**){com_packages}   
        # of module dependencies = **{n_module_deps}**, # of package dependencies = **{n_package_deps}**
        """.format(**locals()))
        return markdown_to_html+PackageDependencyStatsDataframe().data().to_html()+"<br>"+ModuleDependencyStatsDataframe().data().to_html()


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
    # ModuleDependencyStatsDataframe().data()
    # PackageDependencyStatsDataframe().data()
    # DependencyAnalysisObj().data()
    # UMLClassDiagramObj().data()
    # UMLClassRelationDiagramObj().data()
    ModuleRelationGraphObj().data()
    PackageAndModuleRelationsGraphObj().data()
    PackageRelationsGraphObj().data()
    # PackagesImportModuleGraphObj().data()
