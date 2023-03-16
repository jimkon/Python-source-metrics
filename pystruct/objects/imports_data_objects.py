import pandas as pd

from pystruct.html_utils.html_pages import HTMLPage
from pystruct.metrics.import_metrics import enrich_import_raw_df
from pystruct.objects.data_objects import DataframeObject, HTMLTableObject, HTMLObject
from pystruct.objects.metric_obj import IsScriptFile
from pystruct.objects.python_object import PObject
from pystruct.reports.import_graph import CollectImportsVisitor


class ImportsRawDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None}, to_csv_kwargs={'index': False})

    def build(self):
        pobj = PObject().python_source_object()
        imports_col = CollectImportsVisitor()
        pobj.use_visitor(imports_col)
        return imports_col.result()


class ImportsEnrichedDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None}, to_csv_kwargs={'index': False})

    def build(self):
        df = ImportsRawDataframe().data()

        df_enriched = enrich_import_raw_df(df)
        df_enriched = df_enriched.merge(IsScriptFile().data(),
                                        left_on='module',
                                        right_on='item',
                                        how='left').drop(columns=['item'])

        return df_enriched


class MostImportedPackages(HTMLTableObject):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        value_counts = df['import_root'].value_counts()
        res_df = pd.DataFrame({
            "import_root": value_counts.index,
            '#_of_imports': value_counts.values
        })
        return res_df


class MostImportedProjectModules(HTMLTableObject):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        value_counts = df['import_module'].value_counts()
        res_df = pd.DataFrame({
            "import_module": value_counts.index,
            '#_of_imports': value_counts.values
        })
        return res_df


class MostImportedProjectPackages(HTMLTableObject):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        value_counts = df['import_package'].value_counts()
        res_df = pd.DataFrame({
            "import_package": value_counts.index,
            '#_of_imports': value_counts.values
        })
        return res_df


class UnusedModules(HTMLTableObject):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        df = df[df['module_name'] != '__init__']
        return df[df['unused_module']][['module', 'is_script_file']].drop_duplicates()


class InvalidImports(HTMLTableObject):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        filtered_df = df[df['invalid_import']]
        return filtered_df[['module', 'imports']]


class InProjectImportModuleGraphDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None}, to_csv_kwargs={'index': False})

    def build(self):
        df = ImportsEnrichedDataframe().data()

        df_graph = df[df['is_project_module']][['module', 'import_module']].drop_duplicates()

        return df_graph


class PackagesImportModuleGraphDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None}, to_csv_kwargs={'index': False})

    def build(self):
        df = ImportsEnrichedDataframe().data()

        df_graph = df[~(df['is_project_module']) & ~(df['imports'] == 'no-imports')][['module', 'import_root']].drop_duplicates()

        return df_graph


class ImportsStatsHTML(HTMLObject):
    def build(self):
        page = HTMLPage()
        page.add_element(MostImportedPackages().data())
        page.add_element(MostImportedProjectModules().data())
        page.add_element(MostImportedProjectPackages().data())
        page.add_element(UnusedModules().data())
        page.add_element(InvalidImports().data())
        return page.html()


if __name__ == "__main__":
    # ImportsEnrichedDataframe().data()
    # MostImportedPackages().data()
    # MostImportedProjectModules().data()
    # MostImportedProjectPackages().data()
    # UnusedModules().data()
    # InvalidImports().data()
    InProjectImportModuleGraphDataframe().data()
    PackagesImportModuleGraphDataframe().data()
