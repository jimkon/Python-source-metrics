import os.path
from functools import lru_cache

from src.configs import PATH_FILES_DIR
from src.utils import path_utils
from src.utils.data_objects import AbstractObject


class GrabCode:
    def __init__(self, path):
        self._path = path
        self.copy_all_python_files()

    @property
    def _base_dir(self):
        return os.path.dirname(self._path)

    @property
    def _working_dir(self):
        return os.path.join(self._base_dir, PATH_FILES_DIR, 'code_copy')

    @lru_cache
    def _grab_all_python_paths(self):
        all_filenames = path_utils.get_all_filenames_in_directory(self._path)
        return path_utils.filter_filenames_by_extension(all_filenames, '.py')

    @lru_cache
    def _calculate_all_new_python_paths(self):
        return [python_path.replace(self._base_dir, self._working_dir)
                for python_path in self._grab_all_python_paths()]

    def copy_all_python_files(self):
        for original_python_file, new_python_file\
                in zip(self._grab_all_python_paths(), self._calculate_all_new_python_paths()):
            path_utils.copy_file_from_to(original_python_file, new_python_file)
