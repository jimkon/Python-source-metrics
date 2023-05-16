import os
import unittest
from unittest import mock

from pystruct.utils import paths


class TestPythonUtils(unittest.TestCase):
    def test__validate_path(self):
        with mock.patch('os.path.exists') as mock_os_exists:
            mock_os_exists.side_effect = lambda x: {
                r'C:\a': True,
                r'C:\b': False,
            }[x]
            try:
                paths._validate_path(r'C:\a')
            except FileNotFoundError:
                self.assertTrue(False)

            self.assertRaises(FileNotFoundError, paths._validate_path, r'C:\b')

    def test__last_path_part(self):
        self.assertEqual(paths._last_path_part(os.sep.join(['a'])), 'a')
        self.assertEqual(paths._last_path_part(os.sep.join(['a', 'b'])), 'b')
        self.assertEqual(paths._last_path_part(os.sep.join(['a', 'b', 'c'])), 'c')
        self.assertEqual(paths._last_path_part(os.sep.join(['a', 'b', 'c.ext'])), 'c.ext')

    def test_Path(self):
        with mock.patch('pystruct.utils.paths._validate_path') as mock_val:
            with mock.patch('os.path.isdir') as mock_os_isdir:
                mock_os_isdir.side_effect = lambda x: {
                    r'C:\a\b\c': True,
                    r'C:\a\b\c\c1': True,
                    r'C:\a\b\c\c2': True,
                    r'C:\a\b\c\c3.ext': False
                }[x]

                with mock.patch('os.listdir') as mock_os_ls:
                    mock_os_ls.return_value = ['c1', 'c2', 'c3.ext']

                    p = paths.Path('C://a//b//c')
                    self.assertEqual(p.abspath, r'C:\a\b\c')
                    self.assertEqual(p.relpath, 'c')
                    self.assertEqual(p.is_directory, True)
                    self.assertEqual(p.is_file, False)
                    self.assertEqual(p.dotted_relpath, 'c')
                    self.assertEqual(p.name, 'c')
                    self.assertTrue(isinstance(p.sub_paths, list))
                    self.assertEqual(str(p), r'c (C:\a\b\c)')

                    p1 = p['c.c1']
                    self.assertEqual(p1.abspath, r'C:\a\b\c\c1')
                    self.assertEqual(p1.relpath, 'c\c1')
                    self.assertEqual(p1.is_directory, True)
                    self.assertEqual(p1.is_file, False)
                    self.assertEqual(p1.dotted_relpath, 'c.c1')
                    self.assertEqual(p1.name, 'c1')
                    self.assertTrue(isinstance(p1.sub_paths, list))
                    self.assertEqual(str(p1), r'c\c1 (C:\a\b\c\c1)')

                    p2 = p['c.c2']
                    self.assertEqual(p2.abspath, r'C:\a\b\c\c2')
                    self.assertEqual(p2.relpath, 'c\c2')
                    self.assertEqual(p2.is_directory, True)
                    self.assertEqual(p2.is_file, False)
                    self.assertEqual(p2.dotted_relpath, 'c.c2')
                    self.assertEqual(p2.name, 'c2')
                    self.assertTrue(isinstance(p2.sub_paths, list))
                    self.assertEqual(str(p2), r'c\c2 (C:\a\b\c\c2)')

                    p3 = p['c.c3']
                    self.assertEqual(p3.abspath, r'C:\a\b\c\c3.ext')
                    self.assertEqual(p3.relpath, 'c\c3.ext')
                    self.assertEqual(p3.is_directory, False)
                    self.assertEqual(p3.is_file, True)
                    self.assertEqual(p3.name, 'c3')
                    self.assertEqual(p3.sub_paths, None)
                    self.assertEqual(str(p3), r'c\c3.ext (C:\a\b\c\c3.ext)')
