from pystruct.objects.data_objects import JSONObjectABC
from pystruct.plat.dataset_controller import DatasetController
from pystruct.python.python_source_obj import PythonSourceObj


class PObject(JSONObjectABC):
    def __init__(self):
        super().__init__()
        self._pobj = None

    def build(self):
        # srcs = os.listdir(PATH_CODE_COPY_DIR)
        # src_path = os.path.join(PATH_CODE_COPY_DIR, srcs[0])
        code_dir = DatasetController().current_dataset.code_directory
        self._pobj = PythonSourceObj.from_project_source(code_dir)
        return self._pobj.to_dict()

    def python_source_object(self):
        if not self._pobj:
            self._pobj = PythonSourceObj.from_dict(self.data())
        return self._pobj


if __name__ == '__main__':
    # PObject().data()
    PObject().python_source_object()

