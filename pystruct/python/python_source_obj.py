from pystruct.python.basic_structure import TreeNode
from pystruct.python.python_obj_factory import PathObjectFactory, DictObjectFactory
from pystruct.utils.logs import log_cyan
from pystruct.utils.path_utils import load_file_as_string
from pystruct.utils.paths import Path
from pystruct.visitors.init_visitor import PythonObjInitializer
from pystruct.visitors.load_pobj_visitor import LoadObjInitializer
from pystruct.visitors.pobj_to_dict_visitor import ConvertPythonSourceObjToDict
from pystruct.visitors.visitor import VisitedMixin


class PythonSourceObj(VisitedMixin):
    def __init__(self, head):
        self._head = head

    def use_visitor(self, visitor):
        self._head.pre_order_visit(visitor)
        visitor.done()

    def _node(self):
        return self._head

    def to_dict(self):
        store_visitor = ConvertPythonSourceObjToDict()
        self.use_visitor(store_visitor)
        return store_visitor.dict()

    @staticmethod
    def from_project_source(abspath):
        log_cyan(f"Creating Python Source Object from path: {abspath}")
        abspath = Path(abspath)
        obj_factory = PathObjectFactory(abspath)

        if obj_factory.root_path.is_directory:
            head = obj_factory.directory(abspath.dotted_relpath)
        else:
            code = load_file_as_string(abspath.abspath)
            head = obj_factory.module(abspath.dotted_relpath, code)

        python = PythonSourceObj(head)
        python.use_visitor(PythonObjInitializer(obj_factory))

        return python

    @staticmethod
    def from_dict(_dict):
        obj_factory = DictObjectFactory()

        first_key = list(_dict.keys())[0]
        head_obj = obj_factory.node_dict_to_object(first_key, _dict[first_key])
        head = TreeNode(None, head_obj)

        python = PythonSourceObj(head)
        python.use_visitor(LoadObjInitializer(obj_factory, _dict))

        return python



