import pandas as pd

from pystruct.html_utils.html_pages import HTMLPage, TabsHTML
from pystruct.metrics.import_metrics import enrich_import_raw_df
from pystruct.objects.data_objects import DataframeObjectABC, HTMLTableObjectABC, HTMLObjectABC
from pystruct.objects.metric_obj import IsScriptFile
from pystruct.objects.python_object import PObject
from pystruct.python.code_structure import ClassMethodObj
from pystruct.reports.import_graph import CollectImportsVisitor
from pystruct.visitors.visitor import TreeNodeVisitor


class ClassMethodsRawDataframe(DataframeObjectABC):
    class CollectClassMethodsVisitor(TreeNodeVisitor):
        def __init__(self):
            self._class_methods_list = []

        def visit_class_method(self, node):
            class_name = node.parent.data.name
            method = node.data.name.split('.')[-1]
            self._class_methods_list.append({'class': class_name, 'method': method})

        def to_dataframe(self):
            return pd.DataFrame(self._class_methods_list, columns=['class', 'method'])

    def build(self):
        pobj = PObject().python_source_object()
        class_methods = ClassMethodsRawDataframe.CollectClassMethodsVisitor()
        pobj.use_visitor(class_methods)
        return class_methods.to_dataframe()


class ClassMethodsEnrichedDataframe(DataframeObjectABC):
    def build(self):
        df = ClassMethodsRawDataframe().dataframe()
        self.enrich_df(df)
        return df

    def enrich_df(self, df):
        df['visibility'] = df['method'].apply(lambda method: 'private' if method[:2] == '__'
                                                        else 'protected' if method[:1] == '_' else 'public')


if __name__ == '__main__':
    ClassMethodsEnrichedDataframe().dataframe()


class ImportsRawDataframe(DataframeObjectABC):
    def build(self):
        pobj = PObject().python_source_object()
        imports_col = CollectImportsVisitor()
        pobj.use_visitor(imports_col)
        return imports_col.result()


class ImportsEnrichedDataframe(DataframeObjectABC):
    def build(self):
        df = ImportsRawDataframe().data()

        df_enriched = enrich_import_raw_df(df)
        df_enriched = df_enriched.merge(IsScriptFile().data(),
                                        left_on='module',
                                        right_on='item',
                                        how='left').drop(columns=['item'])

        return df_enriched


class MostImportedPackages(HTMLTableObjectABC):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        value_counts = df['import_root'].value_counts()
        res_df = pd.DataFrame({
            "import_root": value_counts.index,
            '#_of_imports': value_counts.values
        })
        return res_df


class MostImportedProjectModules(HTMLTableObjectABC):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        value_counts = df['import_module'].value_counts()
        res_df = pd.DataFrame({
            "import_module": value_counts.index,
            '#_of_imports': value_counts.values
        })
        return res_df


class MostImportedProjectPackages(HTMLTableObjectABC):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        value_counts = df[df['is_internal']]['import_package'].value_counts()
        res_df = pd.DataFrame({
            "import_package": value_counts.index,
            '#_of_imports': value_counts.values
        })
        return res_df


class UnusedModules(HTMLTableObjectABC):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        df = df[df['module_name'] != '__init__']
        return df[df['unused_module']][['module', 'is_script_file']].drop_duplicates()


class InvalidImports(HTMLTableObjectABC):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        filtered_df = df[df['invalid_import']]
        return filtered_df[['module', 'imports']]


class InProjectImportModuleGraphDataframe(DataframeObjectABC):
    def build(self):
        df = ImportsEnrichedDataframe().data()

        df_graph = df[df['is_internal']][['module', 'import_module']].drop_duplicates()

        return df_graph


class PackagesImportModuleGraphDataframe(DataframeObjectABC):
    def build(self):
        df = ImportsEnrichedDataframe().data()

        df_graph = df[~(df['is_internal']) & ~(df['is_no_imports'])][['module', 'import_root']].drop_duplicates()

        return df_graph


class ImportsStatsHTML(HTMLObjectABC):
    def build(self):
        page = TabsHTML()
        page.add_tab(MostImportedPackages.name(), MostImportedPackages().data())
        page.add_tab(MostImportedProjectModules.name(), MostImportedProjectModules().data())
        page.add_tab(MostImportedProjectPackages.name(), MostImportedProjectPackages().data())
        page.add_tab(UnusedModules.name(), UnusedModules().data())
        page.add_tab(InvalidImports.name(), InvalidImports().data())
        return page.html()


if __name__ == "__main__":
    ImportsEnrichedDataframe().data()
    # MostImportedPackages().data()
    # MostImportedProjectModules().data()
    # MostImportedProjectPackages().data()
    # UnusedModules().data()
    # InvalidImports().data()
    # InProjectImportModuleGraphDataframe().data()
    # PackagesImportModuleGraphDataframe().data()
