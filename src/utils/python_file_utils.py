import ast
import os

from src.configs import PYTHON_FILE_EXTENSION
from src.utils.path_utils import break_path_in_parts, filter_filenames_by_extension, get_all_filenames_in_directory, load_file_as_string, \
    remove_path_prefix


def validate_python_path(path):
    _, ext = os.path.splitext(os.path.normpath(path))
    if ext != PYTHON_FILE_EXTENSION:
        raise ValueError(f"Path must be pointing to a python (.py) file. Given: {path}")


def convert_python_path_to_module_name(path):
    filename, ext = os.path.splitext(os.path.normpath(path))
    parts = break_path_in_parts(filename)
    module_name = '.'.join(parts)

    return module_name


def get_all_python_files(path):
    all_filenames = get_all_filenames_in_directory(path)
    python_filenames = filter_filenames_by_extension(all_filenames, PYTHON_FILE_EXTENSION)
    return python_filenames


def load_python_modules(path):
    result_dict = {}

    for filepath in get_all_python_files(path):
        file_content = load_file_as_string(filepath)
        filename = remove_path_prefix(filepath, path)
        result_dict[filename] = file_content
    return result_dict

