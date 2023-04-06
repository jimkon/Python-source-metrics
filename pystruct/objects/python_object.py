import os

from pystruct.configs import PATH_CODE_COPY_DIR
from pystruct.objects.data_objects import AbstractObject
from pystruct.python.python_source_obj import PythonSourceObj
from pystruct.utils.file_strategies import JsonFile


class PObject(AbstractObject):
    def __init__(self):
        super().__init__(JsonFile(self))
        self._pobj = None

    def build(self):
        srcs = os.listdir(PATH_CODE_COPY_DIR)
        src_path = os.path.join(PATH_CODE_COPY_DIR, srcs[0])
        self._pobj = PythonSourceObj.from_project_source(src_path)
        return self._pobj.to_dict()

    def python_source_object(self):
        if not self._pobj:
            self._pobj = PythonSourceObj.from_dict(self.data())
        return self._pobj


if __name__ == '__main__':
    # PObject().data()
    PObject().python_source_object()

