from pystruct.python.basic_structure import TreeNode
from pystruct.utils.logs import log_cyan
from pystruct.visitors.visitor import TreeNodeVisitor


class LoadObjInitializer(TreeNodeVisitor):

    def __init__(self, obj_factory, _dict):
        self._obj_factory = obj_factory
        self._dict = _dict
        self._parent_dir = self._produce_parent_dir()

    def _produce_parent_dir(self):
        all_nodes = list(self._dict.keys())

        parent_dir = {node: None for node in all_nodes}

        for node in all_nodes:
            for cnodes in self._dict[node]['branches']:
                parent_dir[cnodes] = node

    def visit_all(self, node):
        node_name = node.data.name
        obj_dict = self._dict[node_name]
        node_type = self._dict[node_name]['type']
        log_cyan(f".Reading {node_type} {node}", verbosity=3)

        list_objs = []
        for sub_node_name in obj_dict['branches']:
            sub_obj_dict = self._dict[sub_node_name]
            sub_obj = self._obj_factory.node_dict_to_object(sub_node_name, sub_obj_dict)
            list_objs.append(TreeNode(node, sub_obj))

        node.set_branches(list_objs)
        log_cyan(f"_Init {node_type}:{node.data.name} branches ({len(list_objs)})", verbosity=3)
