import json
import os
import tempfile
import unittest

from pystruct.python.python_source_obj import PythonSourceObj

a_py_file_content = """
import one_package
from another_package import that_module

def a_function(some, arguments):
    var = "something"
    return var

class a_class:
    def a_class_method(self):
        return 1

"""

# expected_dict_str = r"""{"pystruct": {"type": "directory", "code": null, "branches": ["pystruct.a"]}, "pystruct.a": {"type": "module", "code": "\nimport one_package\nfrom another_package import that_module\n\ndef a_function(some, arguments):\n    var = \"something\"\n    return var\n\nclass a_class:\n    def a_class_method(self):\n        return 1\n\n", "branches": ["pystruct.a.a_function", "pystruct.a.a_class"]}, "pystruct.a.a_function": {"type": "function", "code": "def a_function(some, arguments):\n    var = \"something\"\n    return var", "branches": []}, "pystruct.a.a_class": {"type": "class", "code": "class a_class:\n    def a_class_method(self):\n        return 1", "branches": ["pystruct.a.a_class.a_class_method"]}, "pystruct.a.a_class.a_class_method": {"type": "class_method", "code": "def a_class_method(self):\n    return 1", "branches": []}}"""


class TestPythonSourceObj(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        with open(os.path.join(self.tmp_dir.name, 'a.py'), 'w') as f:
            f.write(a_py_file_content)

    def test_create_from_project_source(self):
        expected_dict_str = open('/tests/res_files/example_PObject.json').read()
        expected_dict = json.loads(expected_dict_str.replace('pystruct', os.path.basename(self.tmp_dir.name)))

        pobj = PythonSourceObj.from_dict(expected_dict)
        test_dict = pobj.to_dict()

        self.assertEqual(test_dict, expected_dict)

    def test_create_from_dict(self):
        expected_dict_str = open('/tests/res_files/example_PObject.json').read()

        pobj = PythonSourceObj.from_dict(self.tmp_dir.name)

        test_dict = pobj.to_dict()
        expected_dict = json.loads(expected_dict_str.replace('pystruct', os.path.basename(self.tmp_dir.name)))

        self.assertEqual(test_dict, expected_dict)


class TestPythonSourceObjIntegration(unittest.TestCase):
    def setUp(self) -> None:
        path = "../res_files/example_project"
        self.pso = PythonSourceObj.from_project_source(path)
        self.pso_dict = self.pso.to_dict()
        self.expected_dict = json.loads(open('../res_files/example_PObject.json').read())
        self.maxDiff = None

    def test_directories(self):
        type = 'directory'
        example_obj = {k: v for k, v in self.pso_dict.items() if v['type'] == type}
        expected_obj = {k: v for k, v in self.expected_dict.items() if v['type'] == type}
        self.assertDictEqual(example_obj, expected_obj)

    def test_modules(self):
        type = 'module'
        example_obj = {k: v for k, v in self.pso_dict.items() if v['type'] == type}
        expected_obj = {k: v for k, v in self.expected_dict.items() if v['type'] == type}
        self.assertDictEqual(example_obj, expected_obj)

    def test_functions(self):
        type = 'function'
        example_obj = {k: v for k, v in self.pso_dict.items() if v['type'] == type}
        expected_obj = {k: v for k, v in self.expected_dict.items() if v['type'] == type}
        self.assertDictEqual(example_obj, expected_obj)

    def test_classes(self):
        type = 'class'
        example_obj = {k: v for k, v in self.pso_dict.items() if v['type'] == type}
        expected_obj = {k: v for k, v in self.expected_dict.items() if v['type'] == type}
        self.assertDictEqual(example_obj, expected_obj)

    def test_result(self):
        self.assertDictEqual(self.pso_dict, self.expected_dict)


if __name__ == '__main__':
    unittest.main()
