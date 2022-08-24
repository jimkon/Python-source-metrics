import os.path
from functools import lru_cache

from src.configs import PATH_CODE_COPY_DIR
from src.utils import path_utils


def grab_code(src_path):
    gc = GrabCode(src_path)
    return gc.working_dir


class GrabCode:
    def __init__(self, path):
        self._path = path
        self.copy_all_python_files()

    @property
    def _base_dir(self):
        return os.path.dirname(self._path)

    @property
    def working_dir(self):
        return os.path.join(self._base_dir, PATH_CODE_COPY_DIR)

    @lru_cache
    def _grab_all_python_paths(self):
        if os.path.isfile(self._path):
            all_filenames = [self._path]
        else:
            all_filenames = path_utils.get_all_filenames_in_directory(self._path)
        return path_utils.filter_filenames_by_extension(all_filenames, '.py')

    @lru_cache
    def _calculate_all_new_python_paths(self):
        if self._base_dir == '':
            return [os.path.join(self.working_dir, os.path.basename(python_path))
             for python_path in self._grab_all_python_paths()]

        return [python_path.replace(self._base_dir, self.working_dir)
                for python_path in self._grab_all_python_paths()]

    def copy_all_python_files(self):
        for original_python_file, new_python_file\
                in zip(self._grab_all_python_paths(), self._calculate_all_new_python_paths()):
            path_utils.copy_file_from_to(original_python_file, new_python_file)
