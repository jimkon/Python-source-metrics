import pandas as pd

from src.metrics.import_metrics import enrich_import_raw_df
from src.objects.data_objects import DataframeObject, HTMLTableObject
from src.objects.metric_obj import IsScriptFile, TypeMetricObj
from src.objects.python_object import PObject
from src.reports.import_graph import CollectImportsVisitor


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
        return df[df['unused_module']][['module', 'is_script_file']].drop_duplicates()


class InvalidImports(HTMLTableObject):
    def build_dataframe(self):
        df = ImportsEnrichedDataframe().data()
        filtered_df = df[df['invalid_import']]
        return filtered_df[['module', 'imports']]


if __name__ == "__main__":
    ImportsEnrichedDataframe().data()
    MostImportedPackages().data()
    MostImportedProjectModules().data()
    MostImportedProjectPackages().data()
    UnusedModules().data()
    InvalidImports().data()
