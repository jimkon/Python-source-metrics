import unittest
from unittest import mock

import pandas as pd

from pystruct.objects.dependencies import ModuleDependencyStatsDataframe
from pystruct.objects.imports_data_objects import ImportsEnrichedDataframe


class TestModuleDependencyStatsDataframe(unittest.TestCase):
    @mock.patch.object(ImportsEnrichedDataframe, '__new__')
    def test_external_packages(self, mock_imports):
        test_df = pd.DataFrame({
            'module': ['a1', 'a1', 'a1', 'a1.b1', 'a2', 'a2', 'a2', 'a2', 'a3'],
            'import_package': ['ext_1', 'ext_1', 'ext_2', 'ext_1', 'ext_1', 'ext_2', 'int_1', 'ext_3', 'int_2'],
            'is_external': [True, True, True, True, True, True, False, True, False],
        })
        expected_df = pd.DataFrame({
            'module': ['a1', 'a1.b1', 'a2'],
            'external_packages': [['ext_1', 'ext_2'], ['ext_1'], ['ext_1', 'ext_2', 'ext_3']],
            'number_of_external_packages': [2, 1, 3],
        }).set_index('module')

        obj = ModuleDependencyStatsDataframe()
        obj._imports_df = test_df
        pkg_deps = obj.produce_external_packages()
        pd.testing.assert_frame_equal(pkg_deps, expected_df)

    @mock.patch.object(ImportsEnrichedDataframe, '__new__')
    def test_python_builtin_packages(self, mock_imports):
        test_df = pd.DataFrame({
            'module': ['a1', 'a1', 'a1', 'a2', 'a2', 'a2', 'a2', 'a2', 'a3'],
            'import_package': ['ext_1', 'ext_1', 'ext_2', 'ext_1', 'ext_1', 'ext_2', 'builtin_1', 'builtin_2', 'builtin_1'],
            'is_builtin': [False, False, False, False, False, False, True, True, True],
        })
        expected_df = pd.DataFrame({
            'module': ['a2', 'a3'],
            'builtin_packages': [['builtin_1', 'builtin_2'], ['builtin_1']],
            'number_of_builtin_packages': [2, 1],
        }).set_index('module')
        obj = ModuleDependencyStatsDataframe()
        obj._imports_df = test_df
        pkg_deps = obj.produce_python_builtin_packages()
        pd.testing.assert_frame_equal(pkg_deps, expected_df)

    @mock.patch.object(ImportsEnrichedDataframe, '__new__')
    def test_internal_packages(self, mock_imports):
        test_df = pd.DataFrame({
            'module': ['a1', 'a1', 'a1', 'a2', 'a2', 'a2', 'a2', 'a2', 'a3'],
            'import_package': ['ext_1', 'ext_1', 'ext_2', 'int_1', 'int_2', 'ext_2', 'int_1', 'ext_3', 'int_2'],
            'is_internal': [False, False, False, True, True, False, True, False, True],
        })
        expected_df = pd.DataFrame({
            'module': ['a2', 'a3'],
            'internal_packages': [['int_1', 'int_2'], ['int_2']],
            'number_of_internal_packages': [2, 1],
        }).set_index('module')
        obj = ModuleDependencyStatsDataframe()
        obj._imports_df = test_df
        pkg_deps = obj.produce_internal_packages()
        pd.testing.assert_frame_equal(pkg_deps, expected_df)

    @mock.patch.object(ImportsEnrichedDataframe, '__new__')
    def test_internal_modules(self, mock_imports):
        test_df = pd.DataFrame({
            'module': ['a1', 'a1', 'a1', 'a2', 'a2', 'a2', 'a2', 'a2', 'a3'],
            'import_module': ['ext_1', 'ext_1', 'ext_2', 'int_1', 'int_2', 'ext_2', 'int_1', 'ext_3', 'int_2'],
            'is_internal': [False, False, False, True, True, False, True, False, True],
        })
        expected_df = pd.DataFrame({
            'module': ['a2', 'a3'],
            'internal_modules': [['int_1', 'int_2'], ['int_2']],
            'number_of_internal_modules': [2, 1],
        }).set_index('module')
        obj = ModuleDependencyStatsDataframe()
        obj._imports_df = test_df
        pkg_deps = obj.produce_internal_modules()
        pd.testing.assert_frame_equal(pkg_deps, expected_df)

    @mock.patch.object(ImportsEnrichedDataframe, '__new__')
    def test_imported_from_packages(self, mock_imports):
        test_df = pd.DataFrame({
            'package': ['a1', 'a1', 'a1', 'a2', 'a2', 'a2', 'a2', 'a2', 'a3'],
            'import_module': ['ext_1', 'ext_1', 'ext_2', 'int_1', 'int_2', 'ext_2', 'int_1', 'ext_3', 'int_2'],
            'is_internal': [False, False, False, True, True, False, True, False, True],
        })
        expected_df = pd.DataFrame({
            'module': ['int_1', 'int_2'],
            'imported_from_packages': [['a2'], ['a2', 'a3']],
            'times_been_imported_from_packages': [1, 2],
        }).set_index('module')
        obj = ModuleDependencyStatsDataframe()
        obj._imports_df = test_df
        pkg_deps = obj.produce_imported_from_packages()
        pd.testing.assert_frame_equal(pkg_deps, expected_df)

    @mock.patch.object(ImportsEnrichedDataframe, '__new__')
    def test_imported_from_modules(self, mock_imports):
        test_df = pd.DataFrame({
            'module': ['a1', 'a1', 'a1', 'a2', 'a2', 'a2', 'a2', 'a2', 'a3'],
            'import_module': ['ext_1', 'ext_1', 'ext_2', 'int_1', 'int_2', 'ext_2', 'int_1', 'ext_3', 'int_2'],
            'is_internal': [False, False, False, True, True, False, True, False, True],
        })
        expected_df = pd.DataFrame({
            'module': ['int_1', 'int_2'],
            'imported_from_modules': [['a2'], ['a2', 'a3']],
            'times_been_imported_from_modules': [1, 2],
        }).set_index('module')
        obj = ModuleDependencyStatsDataframe()
        obj._imports_df = test_df
        pkg_deps = obj.produce_imported_from_modules()
        pd.testing.assert_frame_equal(pkg_deps, expected_df)


if __name__ == '__main__':
    unittest.main()

