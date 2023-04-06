import pandas as pd

from pystruct.objects.imports_data_objects import ImportsEnrichedDataframe
from pystruct.objects.data_objects import DataframeObject
from pystruct.utils.python_utils import is_python_builtin_package


def _produce_unique_and_nunique_from_df(imports_df, new_column_name, groupby_column, agg_column):
    agg_rows = imports_df.groupby(groupby_column).agg({agg_column: [pd.Series.unique, pd.Series.nunique]})
    agg_rows.columns = [f'{new_column_name}s', f'number_of_{new_column_name}s']
    agg_rows[f'number_of_{new_column_name}s'].fillna(0, inplace=True)
    # agg_rows[f'number_of_{new_column_name}s'] = agg_rows[f'number_of_{new_column_name}s'].astype(int)
    return agg_rows


class PackageDependencyStatsDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None, 'header': 0}, to_csv_kwargs={'index': False})
        df = ImportsEnrichedDataframe().data()
        df_filtered = df[~df['unused_module']]
        self._imports_df = df_filtered

    def build(self):
        df_ext_packages = self.produce_external_packages()
        df_python_packages = self.produce_python_builtin_packages()
        df_int_packages = self.produce_internal_packages()
        df_cyclic_imports = self.produce_cyclic_imports()
        df_int_modules = self.produce_internal_modules()
        df_imported_from_packages = self.produce_imported_from_packages()

        df_pack_deps = pd.concat([df_ext_packages, df_python_packages, df_int_packages, df_cyclic_imports, df_int_modules, df_imported_from_packages], axis=1)
        df_pack_deps = df_pack_deps.reset_index()
        return df_pack_deps

    def produce_external_packages(self):
        external_modules = self._imports_df[self._imports_df['is_external']]
        return _produce_unique_and_nunique_from_df(external_modules,
                                                   new_column_name='external_package',
                                                   groupby_column='package',
                                                   agg_column='import_package')

    def produce_python_builtin_packages(self):
        python_builtin_modules = self._imports_df[self._imports_df['is_builtin']]
        return _produce_unique_and_nunique_from_df(python_builtin_modules,
                                                   new_column_name='builtin_package',
                                                   groupby_column='package',
                                                   agg_column='import_package')

    def produce_internal_packages(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        return _produce_unique_and_nunique_from_df(internal_modules,
                                                   new_column_name='internal_package',
                                                   groupby_column='package',
                                                   agg_column='import_package')

    def produce_cyclic_imports(self):
        cyclic_imports = self._imports_df[self._imports_df['package'] == self._imports_df['import_package']]
        cyclic_imports_agg = cyclic_imports.groupby('package').agg({'import_package': 'count'})
        cyclic_imports_agg = cyclic_imports_agg.rename(columns={'import_package': 'imports_itself'})[['imports_itself']]
        return cyclic_imports_agg

    def produce_internal_modules(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        return _produce_unique_and_nunique_from_df(internal_modules,
                                                   new_column_name='internal_module',
                                                   groupby_column='package',
                                                   agg_column='import_module')

    def produce_imported_from_packages(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        res = _produce_unique_and_nunique_from_df(internal_modules,
                                                  new_column_name='imports',
                                                  groupby_column='import_package',
                                                  agg_column='package').reset_index()
        res.columns = ['package', 'imported_from_packages', 'times_been_imported_from_packages']
        res = res.set_index('package')
        return res


class ModuleDependencyStatsDataframe(DataframeObject):
    def __init__(self):
        super().__init__(read_csv_kwargs={'index_col': None, 'header': 0}, to_csv_kwargs={'index': False})
        df = ImportsEnrichedDataframe().data()
        df_filtered = df[~df['unused_module']]
        self._imports_df = df_filtered

    def build(self):
        df_ext_packages = self.produce_external_packages()
        df_python_packages = self.produce_python_builtin_packages()
        df_int_packages = self.produce_internal_packages()
        df_int_modules = self.produce_internal_modules()
        df_imported_from_packages = self.produce_imported_from_packages()
        df_imported_from_modules = self.produce_imported_from_modules()

        df_mod_deps = pd.concat([df_ext_packages, df_python_packages, df_int_packages, df_int_modules, df_imported_from_packages, df_imported_from_modules], axis=1)
        df_mod_deps = df_mod_deps.reset_index()
        return df_mod_deps

    def produce_external_packages(self):
        external_modules = self._imports_df[self._imports_df['is_external']]
        return _produce_unique_and_nunique_from_df(external_modules,
                                                   new_column_name='external_package',
                                                   groupby_column='module',
                                                   agg_column='import_package')

    def produce_python_builtin_packages(self):
        python_builtin_modules = self._imports_df[self._imports_df['is_builtin']]
        return _produce_unique_and_nunique_from_df(python_builtin_modules,
                                                   new_column_name='builtin_package',
                                                   groupby_column='module',
                                                   agg_column='import_package')

    def produce_internal_packages(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        return _produce_unique_and_nunique_from_df(internal_modules,
                                                   new_column_name='internal_package',
                                                   groupby_column='module',
                                                   agg_column='import_package')

    def produce_internal_modules(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        return _produce_unique_and_nunique_from_df(internal_modules,
                                                   new_column_name='internal_module',
                                                   groupby_column='module',
                                                   agg_column='import_module')

    def produce_imported_from_packages(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        res = _produce_unique_and_nunique_from_df(internal_modules,
                                                  new_column_name='imports',
                                                  groupby_column='import_module',
                                                  agg_column='package').reset_index()
        res.columns = ['module', 'imported_from_packages', 'times_been_imported_from_packages']
        res = res.set_index('module')
        return res

    def produce_imported_from_modules(self):
        internal_modules = self._imports_df[self._imports_df['is_internal']]
        res = _produce_unique_and_nunique_from_df(internal_modules,
                                                  new_column_name='imports',
                                                  groupby_column='import_module',
                                                  agg_column='module').reset_index()
        res.columns = ['module', 'imported_from_modules', 'times_been_imported_from_modules']
        res = res.set_index('module')
        return res


if __name__ == '__main__':
    ModuleDependencyStatsDataframe().data()
    PackageDependencyStatsDataframe().data()
