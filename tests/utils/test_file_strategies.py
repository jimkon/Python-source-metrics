import unittest
from unittest.mock import patch

import src.utils.file_strategies as fs


class ExampleObject:
    pass


class ExampleConcreteFileStrategy(fs.AbstractFileStrategy):
    def load_from_file(self, filepath):
        return 'example_data'

    def save_to_file(self, data, filepath):
        pass


class TestAbstractFileStrategy(unittest.TestCase):
    def setUp(self):
        self.example_obj = ExampleObject()
        self.file_strategy = ExampleConcreteFileStrategy(self.example_obj,
                                                         'example_extension')

    def test_filename(self):
        self.assertEqual(self.file_strategy.filename, r"ExampleObject.example_extension")

    def test_filepath(self):
        self.assertEqual(self.file_strategy.filepath, r"example_root_dir\ExampleObject.example_extension")

    def test_load_existing_cached_data(self):
        example_cached_data = 'example_cached_data'
        self.file_strategy._cached_data = example_cached_data

        self.assertEqual(self.file_strategy.load(), example_cached_data)

        self.example_obj._cached_data = None

    def test_load_path_exists(self):
        with patch('os.path.exists') as mock_path_exists:
            mock_path_exists.return_value = True

            self.assertEqual(self.file_strategy.load(), 'example_data')

    def test_load_path_does_not_exist(self):
        with patch('os.path.exists') as mock_path_exists:
            mock_path_exists.return_value = False

            self.assertEqual(self.file_strategy.load(), None)

    def test_save(self):
        with patch.object(ExampleConcreteFileStrategy, 'save_to_file') as mock_save_to_file:
            ExampleConcreteFileStrategy(None, None, None)
            self.file_strategy.save('example_save_data')

            self.assertEqual(self.file_strategy._cached_data, 'example_save_data')
            mock_save_to_file.assert_called_once()
            self.assertEqual(self.file_strategy.load(), 'example_save_data')


if __name__ == '__main__':
    unittest.main()
