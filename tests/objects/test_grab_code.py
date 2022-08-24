import os
import unittest
from unittest.mock import patch, call

from src.objects.grab_code import GrabCode
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
            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode(path)
                self.assertEqual(gc_obj._base_dir, base_dir)

    def test__working_dir(self):
        example_paths_and_working_dirs = [
            ['a/b/c.ext', 'a/b'],
            ['a/b/c', 'a/b'],
            ['a/b', 'a'],
            ['a', ''],
            ['', ''],
        ]
        for path, working_dir in example_paths_and_working_dirs:
            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode(path)
                self.assertEqual(gc_obj._working_dir, os.path.join(working_dir, PATH_CODE_COPY_DIR))

    def test__grab_all_python_paths_nested_dirs(self):
        with patch("src.objects.grab_code.path_utils.get_all_filenames_in_directory") as mock_filenames:
            mock_filenames.return_value = [
                'a.py',
                'b.not_py',
                'temp_dir/a.py',
                'temp_dir/b.not_py',
                'temp_dir/one_more_temp_dir/a.py',
                'temp_dir/one_more_temp_dir/b.not_py'
            ]

            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode('dir_name_not_relevant_to_the_test')
                self.assertEqual(gc_obj._grab_all_python_paths(),
                                 [
                                     'a.py',
                                     'temp_dir/a.py',
                                     'temp_dir/one_more_temp_dir/a.py',
                                 ])

    def test__grab_all_python_paths_single_file(self):
        with patch("src.objects.grab_code.path_utils.get_all_filenames_in_directory") as mock_filenames:
            mock_filenames.return_value = [
                'a.py',
                'b.not_py'
            ]

            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode('dir_name_not_relevant_to_the_test')
                self.assertEqual(gc_obj._grab_all_python_paths(),
                                 [
                                     'a.py'
                                 ])

    def test__grab_all_python_paths_pointing_on_python_file(self):
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode('a.py')
                self.assertEqual(gc_obj._grab_all_python_paths(),
                                 [
                                     'a.py'
                                 ])

    def test__grab_all_python_paths_pointing_on_non_python_file(self):
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.return_value = True
            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode('a.not_py')
                self.assertEqual(gc_obj._grab_all_python_paths(),
                                 [])

    def test__grab_all_python_paths_empty_dir(self):
        with patch("src.objects.grab_code.path_utils.get_all_filenames_in_directory") as mock_filenames:
            mock_filenames.return_value = []

            with patch.object(GrabCode, 'copy_all_python_files'):
                gc_obj = GrabCode('dir_name_not_relevant_to_the_test')
                self.assertEqual(gc_obj._grab_all_python_paths(),
                                 [])

    @patch.object(GrabCode, 'copy_all_python_files')
    @patch.object(GrabCode, '_grab_all_python_paths', return_value=['example_dir/src/a.py'])
    def test__calculate_all_new_python_paths(self, mock_paths, mock_cpy):
        gc_obj = GrabCode('example_dir//src')
        self.assertEqual(gc_obj._base_dir, 'example_dir')
        self.assertEqual(gc_obj._working_dir, os.path.join('example_dir', PATH_CODE_COPY_DIR))

        expected_new_paths = [
            os.path.join('example_dir', PATH_CODE_COPY_DIR, 'src/a.py')
        ]

        for new_path, exp_new_path in zip(gc_obj._calculate_all_new_python_paths(), expected_new_paths):
            self.assertEqual(os.path.normpath(exp_new_path), os.path.normpath(new_path))

    @patch.object(GrabCode, 'copy_all_python_files')
    @patch.object(GrabCode, '_grab_all_python_paths', return_value=['example_dir/a.py'])
    def test__calculate_all_new_python_paths_edge_case(self, mock_paths, mock_cpy):
        gc_obj = GrabCode('example_dir')
        self.assertEqual(gc_obj._base_dir, '')
        self.assertEqual(gc_obj._working_dir, os.path.join(PATH_CODE_COPY_DIR))

        expected_new_paths = [
            os.path.join(PATH_CODE_COPY_DIR, 'a.py')
        ]

        for new_path, exp_new_path in zip(gc_obj._calculate_all_new_python_paths(), expected_new_paths):
            self.assertEqual(os.path.normpath(exp_new_path), os.path.normpath(new_path))

    @patch.object(GrabCode, '_grab_all_python_paths', return_value=['example_dir/src/a.py'])
    @patch.object(GrabCode, '_calculate_all_new_python_paths', return_value=[os.path.join('example_dir', PATH_CODE_COPY_DIR, 'src/a.py')])
    def test_copy_all_python_files(self, mock_grab, mock_calc):
        with patch("src.objects.grab_code.path_utils.copy_file_from_to") as mock_cpy:
            GrabCode('example_dir//src')
            mock_cpy.assert_called_with('example_dir/src/a.py', os.path.join('example_dir', PATH_CODE_COPY_DIR, 'src/a.py'))

    # def test_grab_code_execution(self):
    #     with patch("src.objects.grab_code.path_utils.get_all_filenames_in_directory") as mock_filenames:
    #         mock_filenames.return_value = [
    #             'example_dir/src/a.py',
    #             'example_dir/src/b.not_py',
    #             'example_dir/src/temp_dir/a.py',
    #             'example_dir/src/temp_dir/b.not_py',
    #             'example_dir/src/temp_dir/one_more_temp_dir/a.py',
    #             'example_dir/src/temp_dir/one_more_temp_dir/b.not_py'
    #         ]
    #         with patch("src.objects.grab_code.path_utils.copy_file_from_to") as mock_cpy:
    #             gc = GrabCode('/example_dir/src')
    #             self.assertEqual(gc._base_dir, '/example_dir')
    #             self.assertEqual(gc._working_dir, PATH_CODE_COPY_DIR)
    #             # self.assertEqual(gc._grab_all_python_paths(), ['example_dir/src/a.py',
    #             #                                                'example_dir/src/temp_dir/a.py',
    #             #                                                'example_dir/src/temp_dir/one_more_temp_dir/a.py'])
    #             # self.assertEqual(gc._calculate_all_new_python_paths(), [os.path.join("example_dir", PATH_CODE_COPY_DIR, 'src/a.py'),
    #             #                                                         os.path.join("example_dir", PATH_CODE_COPY_DIR, 'src/temp_dir/a.py'),
    #             #                                                         os.path.join("example_dir", PATH_CODE_COPY_DIR, 'src/temp_dir/one_more_temp_dir/a.py')])
    #
    #             # mock_cpy.assert_has_calls([call('example_dir/a.py',
    #             #                             os.path.join(PATH_CODE_COPY_DIR, 'a.py'))])


if __name__ == '__main__':
    unittest.main()
