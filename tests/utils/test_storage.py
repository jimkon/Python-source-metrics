import os
import pathlib
import shutil
import unittest
from unittest import mock

from pystruct.utils import storage
from pystruct.utils.storage import DatasetsDirectory, Dataset


class TestDirectory(unittest.TestCase):
    def test_directory(self):
        self.assertEqual(storage.Directory('test_dir').path, pathlib.Path('test_dir'))
        self.assertEqual(storage.Directory(pathlib.Path('test_dir')).path, pathlib.Path('test_dir'))


class TestDatasetsDirectory(unittest.TestCase):
    def setUp(self):
        self.datasets_dir_name = "test_datasets"
        self.datasets_dir = DatasetsDirectory(self.datasets_dir_name)
        self.datasets_dir_path = self.datasets_dir.path

    def tearDown(self):
        shutil.rmtree(self.datasets_dir_path)

    def test_reset_current_dataset(self):
        # Test case when there are no datasets in the directory
        self.datasets_dir.reset_current_dataset()
        self.assertIsNone(self.datasets_dir.get_current_dataset())

        # Test case when there is one dataset in the directory
        dataset_name = "test_dataset"
        dataset_path = self.datasets_dir_path / dataset_name
        dataset_path.mkdir()
        self.datasets_dir.reset_current_dataset()
        current_dataset = self.datasets_dir.get_current_dataset()
        self.assertEqual(current_dataset.path, dataset_path)

    def test_set_current_dataset(self):
        # Test with an existing dataset
        existing_dataset_name = "test_dataset"
        existing_dataset_path = self.datasets_dir_path / existing_dataset_name
        existing_dataset_path.mkdir()
        self.datasets_dir.set_current_dataset(existing_dataset_name)
        current_dataset = self.datasets_dir.get_current_dataset()
        self.assertEqual(current_dataset.path, existing_dataset_path)

        # Test with a non-existing dataset
        non_existing_dataset_name = "non_existing_dataset"
        self.datasets_dir.set_current_dataset(non_existing_dataset_name)
        current_dataset = self.datasets_dir.get_current_dataset()
        self.assertEqual(current_dataset.path, existing_dataset_path)

    def test_new_dataset(self):
        dataset_name = "new_dataset"
        dataset = self.datasets_dir.new_dataset(dataset_name)
        dataset_path = self.datasets_dir_path / dataset_name
        self.assertTrue(dataset_path.exists())
        self.assertEqual(dataset.path, dataset_path)
        current_dataset = self.datasets_dir.get_current_dataset()
        self.assertEqual(current_dataset.path, dataset_path)

    def test_delete_dataset(self):
        dataset_name = "test_dataset"
        dataset_path = self.datasets_dir_path / dataset_name
        dataset_path.mkdir()
        self.datasets_dir.set_current_dataset(dataset_name)
        self.datasets_dir.delete_dataset(dataset_name)
        self.assertFalse(dataset_path.exists())
        self.assertIsNone(self.datasets_dir.get_current_dataset())

if __name__ == '__main__':
    unittest.main()
