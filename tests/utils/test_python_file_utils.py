import unittest
from unittest import mock

from src.utils import python_file_utils as pu


class TestPythonUtils(unittest.TestCase):

    def test_validate_python_path(self):
        self.assertRaises(ValueError, pu.validate_python_path, 'c')
        try:
            pu.validate_python_path('c.py')
        except ValueError:
            self.assertTrue(False)

    def test_convert_python_path_to_module_name(self):
        self.assertEqual(pu.convert_python_path_to_module_name("a/b/c.py"), 'a.b.c')
        self.assertEqual(pu.convert_python_path_to_module_name("c.py"), 'c')

    def test_get_all_python_files(self):
        with mock.patch("src.utils.python_file_utils.get_all_filenames_in_directory") as mocker_files:
            mocker_files.return_value = ["a", "a.py", "a/b", "a/b.extension", "a/b/c.py", "a/b/c"]

            self.assertEqual(pu.get_all_python_files(''), ["a.py", "a/b/c.py"])

        with mock.patch("src.utils.python_file_utils.get_all_filenames_in_directory") as mocker_files:
            mocker_files.return_value = ["a", "a/b/d"]

            self.assertEqual(pu.get_all_python_files(''), [])


if __name__ == '__main__':
    unittest.main()
