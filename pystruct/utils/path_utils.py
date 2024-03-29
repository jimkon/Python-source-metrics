import os
import shutil
import stat

from pystruct.configs import PYTHON_FILE_EXTENSION


def load_file_as_string(filepath):
    with open(filepath, 'r') as f:
        s = f.read()
    return s


def get_python_files_and_directories(path):
    all_sub_filenames = [os.path.join(path, filename) for filename in os.listdir(os.path.normpath(path))]
    directories = [filename for filename in all_sub_filenames if os.path.isdir(filename)]
    python_files = filter_filenames_by_extension(all_sub_filenames, PYTHON_FILE_EXTENSION)
    return python_files, directories


def get_all_filenames_in_directory(path):
    all_filenames = list()
    for dirpath, dirnames, filenames in os.walk(path):
        all_filenames += [os.path.normpath(os.path.join(dirpath, file)) for file in filenames]
    return all_filenames


def filter_filenames_by_extension(filenames, extension):
    def filter_function(filename):
        return len(filename) > len(extension) and filename[-len(extension):] == extension

    filtered_filenames = [filename for filename in filenames if filter_function(filename)]
    return filtered_filenames


def remove_path_prefix(path, path_prefix):
    relative_path = os.path.normpath(path.replace(path_prefix, ''))
    clean_relative_path = os.sep.join(break_path_in_parts(relative_path))
    return clean_relative_path


def break_path_in_parts(path):
    norm_path = os.path.normpath(path)
    parts = [part for part in norm_path.split(os.sep) if len(part) > 0]
    return parts


def dotted_repr_of_path(path):
    parts = break_path_in_parts(path)
    dotted = '.'.join(parts)
    return dotted


def remove_first_path_seperator(path):
    parts = break_path_in_parts(path)
    return os.sep.join(parts)


def get_file_extension(path):
    _, ext = os.path.splitext(os.path.normpath(path))
    if ext == '':
        return None
    else:
        return ext


def remove_extension(path):
    ext = get_file_extension(path)
    if ext:
        return path[:-len(ext)]
    else:
        return path


def copy_file_from_to(from_path, to_path):
    with open(from_path, 'r') as f:
        file_content_str = f.read()

    if os.path.isfile(from_path):
        os.makedirs(os.path.dirname(to_path), exist_ok=True)
    else:
        os.makedirs(to_path, exist_ok=True)

    with open(to_path, 'w') as f:
        f.write(file_content_str)


def delete_dir_if_exists(path):
    if not os.path.exists(path):
        return False
    rmtree(path)
    return True


def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)
