import os
import unittest
from unittest import mock

from pystruct.utils import path_utils


class TestFiles(unittest.TestCase):
    def test_get_python_files_and_directories(self):

        with mock.patch('os.listdir') as mock_os_listdir:
            with mock.patch('os.path.isdir') as mock_os_isdir:
                mock_os_isdir.side_effect = lambda x: {
                    'test_path\\dir': True,
                    'test_path\\a.py': False,
                    'test_path\\b.ext': False
                }[x]

                mock_os_listdir.return_value = [
                    'dir', 'a.py', 'b.ext'
                ]
                python_files, directories = path_utils.get_python_files_and_directories("test_path")
                self.assertEqual(python_files, ['test_path\\a.py'])
                self.assertEqual(directories, ['test_path\\dir'])

    def test_get_all_filenames_in_directory(self):
        with mock.patch('os.walk') as mock_os_walk:
            mock_os_walk.return_value = [
                ('.', ['directory'], ['a', 'b']),
                ('.\\directory', [], ['c', 'd'])
            ]

            self.assertEqual(path_utils.get_all_filenames_in_directory('random_dir'),
                             ['a', 'b', 'directory\\c', 'directory\\d'])

    def test_filter_filenames_by_extension(self):
        test_filenames = [
            "/a/b/c",
            "/a/b/c.py",
            "/a/b/c.exe",
            "d.py",
            "\\a\b/c.py"
        ]
        self.assertEqual(path_utils.filter_filenames_by_extension(test_filenames, '.py'),
                         ["/a/b/c.py", 'd.py', "\\a\b/c.py"])
        self.assertEqual(path_utils.filter_filenames_by_extension([], '.py'), [])
        self.assertEqual(path_utils.filter_filenames_by_extension(['a', '/b'], '.py'), [])

    def test_remove_path_prefix(self):
        self.assertEqual(path_utils.remove_path_prefix('/a/b/c/d', 'a'), 'b\\c\\d')
        self.assertEqual(path_utils.remove_path_prefix('a\\b\\c\\d', 'a\\b'), 'c\\d')
        self.assertEqual(path_utils.remove_path_prefix('a/b/c/d', 'a/b/c'), 'd')
        self.assertEqual(path_utils.remove_path_prefix('a/b/c/d', 'a/b/c/d'), '.')

        self.assertEqual(path_utils.remove_path_prefix('a/b/c/d', 'e/f/g'), r'a\b\c\d')

    def test_break_path_in_parts(self):
        self.assertEqual(path_utils.break_path_in_parts('a/b/c'), ['a', 'b', 'c'])
        self.assertEqual(path_utils.break_path_in_parts('a//b//c'), ['a', 'b', 'c'])
        self.assertEqual(path_utils.break_path_in_parts('a\\b//c'), ['a', 'b', 'c'])
        self.assertEqual(path_utils.break_path_in_parts('a'), ['a'])
        self.assertEqual(path_utils.break_path_in_parts('/a/'), ['a'])
        self.assertEqual(path_utils.break_path_in_parts('/a/c.d'), ['a', 'c.d'])

    def test_dotted_repr_of_path(self):
        self.assertEqual(path_utils.dotted_repr_of_path('a/b/c'), 'a.b.c')
        self.assertEqual(path_utils.dotted_repr_of_path('a//b//c'), 'a.b.c')
        self.assertEqual(path_utils.dotted_repr_of_path('a\\b//c'), 'a.b.c')
        self.assertEqual(path_utils.dotted_repr_of_path('a'), 'a')
        self.assertEqual(path_utils.dotted_repr_of_path('/a/'), 'a')
        self.assertEqual(path_utils.dotted_repr_of_path('/a/c.d'), 'a.c.d')

    def test_remove_first_path_seperator(self):
        self.assertEqual(path_utils.remove_first_path_seperator('/a/b/c'), f'a{os.sep}b{os.sep}c')
        self.assertEqual(path_utils.remove_first_path_seperator('a/b/c'), f'a{os.sep}b{os.sep}c')

    def test_get_file_extension(self):
        self.assertEqual(path_utils.get_file_extension('a/b/c.d'), '.d')
        self.assertEqual(path_utils.get_file_extension('a/b/c/d'), None)

    def test_remove_extension(self):
        self.assertEqual(path_utils.remove_extension('a/b/c.d'), 'a/b/c')
        self.assertEqual(path_utils.remove_extension('a/b/c/d'), 'a/b/c/d')


if __name__ == '__main__':
    unittest.main()
