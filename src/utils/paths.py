import os.path
from functools import cached_property

from src.utils import path_utils
from src.visitors.visitor import VisitedMixin, AbstractVisitor


def _validate_path(abspath):
    if not os.path.exists(abspath):
        raise FileNotFoundError


def _last_path_part(path_str):
    return path_utils.break_path_in_parts(path_str)[-1]


class Path(VisitedMixin):
    def __init__(self, abspath, parent=None):
        self._abspath = os.path.normpath(abspath)
        _validate_path(self.abspath)
        relpath = _last_path_part(self._abspath)
        if not parent:
            self._relpath = relpath
        else:
            self._relpath = os.path.join(parent.relpath, relpath)
        self._sub_paths = None

    @property
    def abspath(self):
        return self._abspath

    @property
    def relpath(self):
        return self._relpath

    @property
    def is_directory(self):
        return os.path.isdir(self.abspath)

    @property
    def is_file(self):
        return not self.is_directory

    @cached_property
    def dotted_relpath(self):
        return path_utils.dotted_repr_of_path(path_utils.remove_extension(self.relpath))

    @property
    def name(self):
        return self.dotted_relpath.split('.')[-1]

    @cached_property
    def sub_paths(self):
        if self.is_directory:
            _res = []
            for _path in os.listdir(self.abspath):
                _abspath = os.path.join(self.abspath, _path)
                _res.append(Path(_abspath, parent=self))
            self._sub_paths = _res
        return self._sub_paths

    def __getitem__(self, item):
        for _path in self.sub_paths:
            last_part = _path.dotted_relpath
            if last_part == item:
                return _path
        return None

    def __str__(self):
        return f"{self.relpath} ({self.abspath})"

