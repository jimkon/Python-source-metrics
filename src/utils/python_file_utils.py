import os

import pandas as pd

from src.configs import PYTHON_FILE_EXTENSION
from src.utils.logs import log_cyan
from src.utils.path_utils import break_path_in_parts, filter_filenames_by_extension, get_all_filenames_in_directory, \
    load_file_as_string, \
    remove_path_prefix, get_file_extension


def is_python_file(path):
    ext = get_file_extension(path)
    if ext == PYTHON_FILE_EXTENSION:
        return True
    return False


def validate_python_path(path):
    if is_python_file(path):
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


def find_source_dirs(path, remove_tests=True, packages_only=True):
    df = pd.DataFrame({'fullpath': get_all_python_files(path)})
    df['relative_path'] = df['fullpath'].apply(lambda filepath: remove_path_prefix(filepath, path))
    df['relative_root_path'] = df['relative_path'].apply(lambda filepath: break_path_in_parts(filepath)[0])
    df['root_fullpath'] = list(map(lambda fullpath, relative_path, relative_root_path: fullpath.replace(relative_path, relative_root_path) , df['fullpath'], df['relative_path'], df['relative_root_path']))
    df['filename'] = df['relative_path'].apply(os.path.basename)
    df['dir_fullpath'] = df['fullpath'].apply(os.path.dirname)
    df['is_init_file'] = df['filename'] == '__init__.py'
    df['is_tests_dir'] = df['relative_path'].apply(lambda filepath: 'tests' in break_path_in_parts(filepath))
    df['is_test_file'] = df['filename'].apply(lambda filepath: 'test_' in filepath)
    df['is_in_package'] = df['dir_fullpath'].isin(df[df['is_init_file']]['dir_fullpath'])

    if remove_tests:
        df = df[(~df['is_tests_dir']) & (~df['is_test_file'])]

    if packages_only:
        df = df[df['is_in_package']]

    log_cyan(df['root_fullpath'].value_counts().head())

    df_group = df.groupby('root_fullpath')['fullpath'].apply(list).reset_index()
    df_group['len'] = df_group['fullpath'].apply(len)

    res_df = df_group.sort_values(by='len', ascending=False)[['root_fullpath', 'fullpath']].set_index(keys=['root_fullpath'])

    return res_df.to_dict('index')


if __name__ == "__main__":
    # temp_dir = clone_code_in_temp_dir("https://github.com/scikit-learn/scikit-learn.git")
    find_source_dirs(r"C:\Users\jim\PycharmProjects\Python-source-metrics\report_files\git")


