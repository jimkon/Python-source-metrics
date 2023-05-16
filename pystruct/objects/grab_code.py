import os.path
from functools import lru_cache

from git import Repo

from pystruct.configs import PATH_CODE_COPY_DIR, PATH_FILES_DIR, PATH_GIT_COPY_DIR
from pystruct.utils import path_utils
from pystruct.utils.logs import log_yellow, log_cyan, log_red, log_pink
from pystruct.utils.path_utils import delete_dir_if_exists
from pystruct.utils.python_file_utils import find_source_dirs


def is_git_url(url):
    if url.startswith("https://github.com/") and url.endswith(".git"):
        return True
    return False


def grab_code(path):
    if is_git_url(path):
        # with tempfile.TemporaryDirectory(prefix="git_clone_") as temp_dir:
        log_pink(f"Cloning repo: {path} ...")
        delete_dir_if_exists(PATH_GIT_COPY_DIR)
        Repo.clone_from(path, PATH_GIT_COPY_DIR)
        log_pink(f"Repo {path} cloned into path: {PATH_GIT_COPY_DIR}")
        CopyCode.extract_all_source_dirs_from_path(PATH_GIT_COPY_DIR)
    else:
        CopyCode(path)
    # CopyCode.extract_all_source_dirs_from_path(dir_to_grab)
    return PATH_FILES_DIR


class CopyCode:
    def __init__(self, path, python_filpaths=None):
        self._path = path
        self._python_filpaths = python_filpaths if python_filpaths else self._grab_all_python_paths()
        log_yellow(f"Coping {len(self.all_python_filepaths)} source files from {path}.")
        delete_dir_if_exists(PATH_CODE_COPY_DIR)
        self.copy_all_python_files()
        log_cyan(f"Copied {len(self.all_python_filepaths)} source files from {path}.")


    @property
    def _base_dir(self):
        return os.path.dirname(self._path)

    @property
    def _working_dir(self):
        return PATH_CODE_COPY_DIR

    @property
    def all_python_filepaths(self):
        return self._python_filpaths

    @lru_cache
    def _grab_all_python_paths(self):
        if os.path.isfile(self._path):
            all_filenames = [self._path]
        else:
            all_filenames = path_utils.get_all_filenames_in_directory(self._path)
        all_python_filenames = path_utils.filter_filenames_by_extension(all_filenames, '.py')
        return all_python_filenames

    @lru_cache
    def _calculate_all_new_python_paths(self):
        if self._base_dir == '':
            return [os.path.join(self._working_dir, os.path.basename(python_path))
                    for python_path in self.all_python_filepaths]

        return [python_path.replace(self._base_dir, self._working_dir)
                for python_path in self.all_python_filepaths]

    def copy_all_python_files(self):
        for original_python_file, new_python_file\
                in zip(self.all_python_filepaths, self._calculate_all_new_python_paths()):
            try:
                path_utils.copy_file_from_to(original_python_file, new_python_file)
            except UnicodeDecodeError as ude:
                log_red(f"Failed to copy file {original_python_file} to {new_python_file}.\n")
                log_red(f"{ude}")

    @staticmethod
    def extract_all_source_dirs_from_path(path, **kwargs):
        res_dict = find_source_dirs(path, **kwargs)
        return [CopyCode(src_dir, python_filepaths['fullpath']) for src_dir, python_filepaths in res_dict.items()]


if __name__ == "__main__":
    # grab_code('https://github.com/jimkon/Python-source-metrics.git')
    grab_code("/Users/dkontzedakis/PycharmProjects/Python-source-metrics/pystruct")
    # CopyCode(r"C:\Users\jim\PycharmProjects\Python-source-metrics\pystruct")
