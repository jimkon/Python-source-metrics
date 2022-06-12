import ast
from functools import cached_property, lru_cache

from src.utils.storage_mixins import StoreClassUML
from src.visitors.visitor import TreeNodeVisitor


class PlantUMLDocument:
    def __init__(self):
        self._res_string = ""
        self._ident = 0
        self._start_uml()

    def _add_line(self, line=''):
        self._res_string += ("\t" * self._ident) + line + "\n"

    def _end_brackets(self):
        self._ident -= 1
        self._add_line('}')

    def _start_uml(self):
        self._add_line('@startuml')
        self._add_line('left to right direction')
        # self._add_line('scale max 1024 width')

    def _end_uml(self):
        self._add_line('@enduml')

    def _start_class(self, class_name):
        self._add_line(f"class {class_name}" + "{")
        self._ident += 1

    def _start_module(self, module_name):
        self._add_line(f"package {module_name} <<Rectangle>>" + "{")
        self._ident += 1

    def _start_package(self, package_name):
        self._add_line(f"package {package_name} <<Folder>>" + "{")
        self._ident += 1

    def add_package(self, package_name, package):
        self._start_package(package_name)
        for module_name, module in package.items():
            self.add_module(module_name, module)
        self._end_brackets()

    def add_module(self, module_name, module):
        self._start_module(module_name)
        for _class in module:
            self.add_class(_class)
        self._end_brackets()

    def add_class(self, class_obj):
        self._start_class(class_obj.name)
        self.add_fields(class_obj.fields)
        self._add_line("==")
        self.add_funtions(class_obj.public_functions)
        self._end_brackets()
        self._add_line()

    def add_fields(self, fields):
        for field in fields:
            self._add_line("{field} " + field)

    def add_funtions(self, functions):
        for function in functions:
            self._add_line("{method} " + function + "()")

    def finish_and_return(self):
        self._end_uml()
        return self._res_string


class UMLClassBuilder:
    def __init__(self):
        self._packages = {}
        self._uml_doc = PlantUMLDocument()

    def add_package(self, package_name):
        if package_name not in self._packages.keys():
            self._packages[package_name] = {}

    def add_module(self, module_name, package_name):
        if module_name not in self._packages[package_name].keys():
            self._packages[package_name][module_name] = []

    def add_class(self, node):
        c = UMLClass(node)

        self.add_package(c.package_name)
        self.add_module(c.module_name, c.package_name)
        self._packages[c.package_name][c.module_name].append(c)

    def result(self):
        for package_name, package_dict in self._packages.items():
            self._uml_doc.add_package(package_name, package_dict)

        return self._uml_doc.finish_and_return()


class UMLClassRelationBuilder:
    def build_class(self, node):
        pass


class UMLClass:
    def __init__(self, node):
        self._node = node
        self._ast = node.data.ast

    @property
    def _class_def(self):
        return self._ast[1]

    @lru_cache
    def _break_name_into_comps(self):
        full_name = self._node.data.name
        parts = full_name.split(".")
        name = parts[-1]
        module_name = parts[-2] if len(parts) > 1 else 'unknown_module'
        package_name = '.'.join(parts[:-2]) if len(parts) > 2 else 'unknown_package'
        return package_name, module_name, name

    @cached_property
    def name(self):
        inheritances_str = f"({','.join(self.inheritances)})" if len(self.inheritances)>0 else ''
        return f"{self._class_def.name}{inheritances_str}"

    @cached_property
    def module_name(self):
        return self._break_name_into_comps()[1]

    @cached_property
    def package_name(self):
        return self._break_name_into_comps()[0]

    @cached_property
    def inheritances(self):
        bases = self._class_def.bases
        res = []
        for base in bases:
            if hasattr(base, 'id'):
                res.append(base.id)
            elif hasattr(base, 'value'):
                res.append(f"{base.value.id}_{base.attr}")
        return res

    @cached_property
    def is_abstract(self):
        return False    # TODO to implement

    @cached_property
    def functions(self):
        inners = self._class_def.body
        return [inner.name for inner in inners if isinstance(inner, ast.FunctionDef)]

    @cached_property
    def public_functions(self):
        return [function for function in self.functions if function[0] != '_']   # TODO to implement

    @cached_property
    def fields(self):
        return []  # TODO to implement


class ClassVisitor(TreeNodeVisitor, StoreClassUML):
    def __init__(self):
        self._uml_class = UMLClassBuilder()

    def visit_class(self, node):
        self._uml_class.add_class(node)

    def data_to_store(self):
        return self._uml_class.result()

