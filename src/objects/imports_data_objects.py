from src.objects.data_objects import AbstractObject
from src.objects.python_object import PObject
from src.reports.import_graph import ImportGraphVisitor
from src.utils.file_strategies import DataframeFile


class ImportsRawDataframe(AbstractObject):
    def __init__(self):
        super().__init__(DataframeFile(self, save_kwargs={'index': False}, load_kwargs={'index_col': None}))

    def build(self):
        pobj = PObject().python_source_object()
        imports_col = ImportGraphVisitor()
        pobj.use_visitor(imports_col)
        return imports_col.result()


if __name__ == "__main__":
    print(ImportsRawDataframe().data().head())
