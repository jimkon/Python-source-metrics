import os
import tempfile
import unittest
from unittest.mock import patch, call

from src.objects.grab_code import CopyCode
from src.configs import PATH_CODE_COPY_DIR


class TestGrabCode(unittest.TestCase):
    def test__base_dir(self):
        example_paths_and_base_dirs = [
            ['a/b/c.ext', 'a/b'],
            ['a/b/c', 'a/b'],
            ['a/b', 'a'],
            ['a', ''],
            ['', ''],
        ]
        for path, base_dir in example_paths_and_base_dirs:
            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(path)
                test_value, expected_value = gc_obj._base_dir, base_dir
                self.assertEqual(test_value, expected_value)

    def test__working_dir(self):
        example_paths_and_working_dirs = [
            ['a/b/c.ext', 'a/b'],
            ['a/b/c', 'a/b'],
            ['a/b', 'a'],
            ['a', ''],
            ['', ''],
        ]
        for path, working_dir in example_paths_and_working_dirs:
            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(path)
                test_value, expected_value = gc_obj._working_dir, PATH_CODE_COPY_DIR
                self.assertEqual(test_value, expected_value)

    @patch.object(CopyCode, 'copy_all_python_files')
    def test_all_python_filepaths(self, *args):
        example_grab_all_python_paths = ['a.py', 'src/a.py']
        another_example_grab_all_python_paths = ['b.py', 'src/b.py']
        with patch.object(CopyCode, '_grab_all_python_paths', return_value=example_grab_all_python_paths):
            gc_obj = CopyCode("a random path")
            self.assertEqual(gc_obj.all_python_filepaths, example_grab_all_python_paths)

            gc_obj = CopyCode("a random path", python_filpaths=another_example_grab_all_python_paths)
            self.assertEqual(gc_obj.all_python_filepaths, another_example_grab_all_python_paths)

    def test__grab_all_python_paths_nested_dirs(self):
        with tempfile.TemporaryDirectory() as example_dir:
            a = tempfile.NamedTemporaryFile(suffix='_a.py', dir=example_dir)
            b = tempfile.NamedTemporaryFile(suffix='_b.not_py', dir=example_dir)
            temp_dir = tempfile.TemporaryDirectory(dir=example_dir)
            temp_dir_a = tempfile.NamedTemporaryFile(suffix='_a.py', dir=temp_dir.name)
            temp_dir_b = tempfile.NamedTemporaryFile(suffix='_b.not_py', dir=temp_dir.name)
            one_more_temp_dir = tempfile.TemporaryDirectory(dir=temp_dir.name)
            one_more_temp_dir_a = tempfile.NamedTemporaryFile(suffix='_a.py', dir=one_more_temp_dir.name)
            one_more_temp_dir_b = tempfile.NamedTemporaryFile(suffix='_b.not_py', dir=one_more_temp_dir.name)

            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(example_dir)
                test_value = gc_obj._grab_all_python_paths()
                expected_value = [
                    a.name,
                    temp_dir_a.name,
                    one_more_temp_dir_a.name
                ]
                self.assertEqual(test_value, expected_value)

    def test__grab_all_python_paths_single_file(self):
        with tempfile.TemporaryDirectory() as example_dir:
            a = tempfile.NamedTemporaryFile(suffix='_a.py', dir=example_dir)
            b = tempfile.NamedTemporaryFile(suffix='_b.not_py', dir=example_dir)

            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(example_dir)
                test_value = gc_obj._grab_all_python_paths()
                expected_value = [
                    a.name,
                ]
                self.assertEqual(test_value, expected_value)

    def test__grab_all_python_paths_pointing_on_python_file(self):
        with tempfile.TemporaryDirectory() as example_dir:
            a = tempfile.NamedTemporaryFile(suffix='_a.py', dir=example_dir)

            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(a.name)
                test_value = gc_obj._grab_all_python_paths()
                expected_value = [
                    a.name,
                ]
                self.assertEqual(test_value, expected_value)

    def test__grab_all_python_paths_pointing_on_non_python_file(self):
        with tempfile.TemporaryDirectory() as example_dir:
            b = tempfile.NamedTemporaryFile(suffix='_b.not_py', dir=example_dir)

            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(example_dir)
                test_value = gc_obj._grab_all_python_paths()
                expected_value = []
                self.assertEqual(test_value, expected_value)

    def test__grab_all_python_paths_empty_dir(self):
        with tempfile.TemporaryDirectory() as example_dir:

            with patch.object(CopyCode, 'copy_all_python_files'):
                gc_obj = CopyCode(example_dir)
                test_value = gc_obj._grab_all_python_paths()
                expected_value = []
                self.assertEqual(test_value, expected_value)

    @patch.object(CopyCode, 'copy_all_python_files')
    @patch.object(CopyCode, '_grab_all_python_paths', return_value=['example_dir/src/a.py'])
    def test__calculate_all_new_python_paths(self, mock_paths, mock_cpy):
        gc_obj = CopyCode('example_dir//src')
        self.assertEqual(gc_obj._base_dir, 'example_dir')
        self.assertEqual(gc_obj._working_dir, PATH_CODE_COPY_DIR)

        expected_new_paths = [
            os.path.join(PATH_CODE_COPY_DIR, 'src/a.py')
        ]

        for new_path, exp_new_path in zip(gc_obj._calculate_all_new_python_paths(), expected_new_paths):
            self.assertEqual(os.path.normpath(exp_new_path), os.path.normpath(new_path))

    @patch.object(CopyCode, 'copy_all_python_files')
    @patch.object(CopyCode, '_grab_all_python_paths', return_value=['example_dir/a.py'])
    def test__calculate_all_new_python_paths_edge_case(self, mock_paths, mock_cpy):
        gc_obj = CopyCode('example_dir')
        self.assertEqual(gc_obj._base_dir, '')
        self.assertEqual(gc_obj._working_dir, PATH_CODE_COPY_DIR)

        expected_new_paths = [
            os.path.join(PATH_CODE_COPY_DIR, 'a.py')
        ]

        for new_path, exp_new_path in zip(gc_obj._calculate_all_new_python_paths(), expected_new_paths):
            self.assertEqual(os.path.normpath(exp_new_path), os.path.normpath(new_path))

    @patch.object(CopyCode, '_grab_all_python_paths', return_value=['example_dir/src/a.py'])
    @patch.object(CopyCode, '_calculate_all_new_python_paths', return_value=[os.path.join(PATH_CODE_COPY_DIR, 'src/a.py')])
    def test_copy_all_python_files(self, mock_grab, mock_calc):
        with patch("src.objects.grab_code.path_utils.copy_file_from_to") as mock_cpy:
            CopyCode('example_dir//src')
            mock_cpy.assert_called_with('example_dir/src/a.py', os.path.join(PATH_CODE_COPY_DIR, 'src/a.py'))

    def test_grab_code_execution(self):
        with tempfile.TemporaryDirectory() as dest_dir:
            with patch("src.objects.grab_code.PATH_CODE_COPY_DIR", dest_dir) as mock_dest_dir:
                with tempfile.TemporaryDirectory() as src_dir:
                    open(os.path.join(src_dir, "a.py"), 'w').close()
                    open(os.path.join(src_dir, "b.not_py"), 'w').close()
                    temp_dir = tempfile.TemporaryDirectory(dir=src_dir)
                    open(os.path.join(temp_dir.name, "a.py"), 'w').close()
                    open(os.path.join(temp_dir.name, "b.not_py"), 'w').close()
                    one_more_temp_dir = tempfile.TemporaryDirectory(dir=temp_dir.name)
                    open(os.path.join(one_more_temp_dir.name, "a.py"), 'w').close()
                    open(os.path.join(one_more_temp_dir.name, "b.not_py"), 'w').close()

                    CopyCode(src_dir)

                    test_dir = os.listdir(dest_dir)[0]
                    self.assertEqual(test_dir, os.path.basename(src_dir))

                    test_dir = os.path.join(dest_dir, os.path.basename(src_dir))
                    self.assertEqual(os.listdir(test_dir), ['a.py', os.path.basename(temp_dir.name)])

                    test_dir = os.path.join(test_dir, os.path.basename(temp_dir.name))
                    self.assertEqual(os.listdir(test_dir), ['a.py', os.path.basename(one_more_temp_dir.name)])

                    test_dir = os.path.join(test_dir, os.path.basename(one_more_temp_dir.name))
                    self.assertEqual(os.listdir(test_dir), ['a.py'])


if __name__ == '__main__':
    unittest.main()
