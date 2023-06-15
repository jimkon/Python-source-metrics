import ast

from pystruct.utils.ast_utils import get_first_ast_of_type, separate_statement
from pystruct.utils.logs import log_cyan
from pystruct.utils.path_utils import load_file_as_string
from pystruct.utils.python_file_utils import is_python_file
from pystruct.visitors.visitor import TreeNodeVisitor

# https://python-ast-explorer.com/
class PythonObjInitializer(TreeNodeVisitor):

    def __init__(self, obj_factory):
        self._obj_factory = obj_factory

    def visit_directory(self, node):
        log_cyan(f".Visiting directory {node}", verbosity=3)
        list_objs = []
        for sub_path in node.data.path.sub_paths:
            if is_python_file(sub_path.abspath):
                code = load_file_as_string(sub_path.abspath)
                module_node = self._obj_factory.module(sub_path.dotted_relpath, code, parent=node)
                log_cyan(f"->Extracted module {module_node.data.name}", verbosity=3)
                list_objs.append(module_node)
            elif sub_path.is_directory:
                dir_node = self._obj_factory.directory(sub_path.dotted_relpath, parent=node)
                log_cyan(f"->Extracted directory {dir_node.data.name}", verbosity=3)
                list_objs.append(dir_node)
            else:
                log_cyan(f"(!!) Ignored {sub_path}", verbosity=3)

        node.set_branches(list_objs)
        log_cyan(f"_Init Directory:{node.data.name} branches ({len(list_objs)})", verbosity=3)

    def visit_module(self, node):
        log_cyan(f".Visiting module {node}", verbosity=3)
        asts_to_fetch = {
            # ast.Import: self._obj_factory.import_node,
            # ast.ImportFrom: self._obj_factory.import_node,
            ast.ClassDef: self._obj_factory.class_node,
            ast.FunctionDef: self._obj_factory.function
        }

        list_objs = []

        remaining_code = node.data.code
        fetched_ast = get_first_ast_of_type(remaining_code, asts_to_fetch.keys())

        while fetched_ast:
            fetched_code, remaining_code = separate_statement(remaining_code, fetched_ast)

            factory_method = asts_to_fetch[fetched_ast.__class__]
            obj = factory_method(f"{node.data.name}.{fetched_ast.name}", fetched_code, parent=node)
            log_cyan(f"->Extracted {fetched_ast.__class__} {obj.data.name}", verbosity=3)
            list_objs.append(obj)

            fetched_ast = get_first_ast_of_type(remaining_code, asts_to_fetch)

        node.set_branches(list_objs)
        log_cyan(f"_Init Module:{node.data.name} branches ({len(list_objs)})", verbosity=3)

    def visit_class(self, node):
        log_cyan(f".Visiting class {node}", verbosity=3)
        asts_to_fetch = {
            # ast.ClassDef: self._obj_factory.class_node,
            ast.FunctionDef: self._obj_factory.class_method
        }

        list_objs = []

        remaining_code = node.data.code
        fetched_ast = get_first_ast_of_type(remaining_code, asts_to_fetch.keys())
        while fetched_ast:
            fetched_code, remaining_code = separate_statement(remaining_code, fetched_ast)

            obj = asts_to_fetch[fetched_ast.__class__](f"{node.data.name}.{fetched_ast.name}", fetched_code,
                                                       parent=node)
            log_cyan(f"->Extracted {fetched_ast.__class__} {obj.data.name}", verbosity=3)
            list_objs.append(obj)

            fetched_ast = get_first_ast_of_type(remaining_code, asts_to_fetch)

        node.set_branches(list_objs)
        log_cyan(f"_Init Class:{node.data.name} branches ({len(list_objs)})", verbosity=3)
