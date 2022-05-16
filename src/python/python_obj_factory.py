import os.path

from src.python.code_structure import *
from src.utils.path_utils import remove_first_path_seperator


class ObjectFactory:

    def __init__(self, src_dir):
        self._source_dir = os.path.normpath(src_dir)

    @property
    def source_path(self):
        return self._source_dir

    def calc_filepath(self, filename):
        basepath = os.path.dirname(self.source_path)
        filepath = os.path.join(basepath, filename)
        return filepath

    def _relative_path(self, path):
        norm_path = os.path.normpath(path)
        rel_path = os.path.normpath(norm_path.replace(os.path.dirname(self._source_dir), ''))
        return remove_first_path_seperator(rel_path)

    def directory(self, filename, parent=None):
        return DirectoryObj(self._relative_path(filename), parent)

    def module(self, filename, parent=None):
        validate_python_path(filename)
        code = load_file_as_string(filename)
        return ModuleObj(self._relative_path(filename), code, parent)

    def class_obj(self, filename, code, parent=None):
        return ClassObj(self._relative_path(filename), code, parent)

    def function(self, filename, code, parent=None):
        return FunctionObj(self._relative_path(filename), code, parent)

    def class_method(self, filename, code, parent=None):
        return ClassMethodObj(self._relative_path(filename), code, parent)


