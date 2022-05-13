import ast
import unittest

from src.python import ast_utils
from src.python.ast_utils import InvalidSubclassType


class TestAstUtils(unittest.TestCase):
    def test_analyse_ast(self):
        self.assertTrue(len(ast_utils.analyse_ast("def test_func():pass")) > 0)
        self.assertEqual(ast_utils.analyse_ast("def test_func():"), [])

    def test_remove_first_n_characters(self):
        self.assertEqual(ast_utils.remove_first_n_characters(["1234A", "1234", "12345678", "123"], 4), ["A", "", "5678", ""])

    def test_separate_statement(self):
        test_code = """
def test_func_1():
    pass

def test_func_2():
    pass
"""
        _asts = ast_utils.analyse_ast(test_code)
        test_func_1_ast = _asts[1]
        test_func_1_code, test_code_left = ast_utils.separate_statement(test_code, test_func_1_ast)
        self.assertEqual(test_func_1_code, "def test_func_1():\n    pass")
        self.assertEqual(test_code_left, "\n\ndef test_func_2():\n    pass\n")

        not_a_statement_subclass_ast = _asts[0]
        self.assertRaises(InvalidSubclassType, ast_utils.separate_statement, test_code, not_a_statement_subclass_ast)

    def test_get_first_ast_of_type(self):
        test_code = """
def test_func_1():
    pass

def test_func_2():
    pass
"""
        self.assertIsNotNone(ast_utils.get_first_ast_of_type(test_code, [ast.Module]))
        self.assertIsNotNone(ast_utils.get_first_ast_of_type(test_code, [ast.FunctionDef]))
        self.assertIsNotNone(ast_utils.get_first_ast_of_type(test_code, [ast.For, ast.FunctionDef]))
        self.assertIsNone(ast_utils.get_first_ast_of_type(test_code, [ast.For]))


if __name__ == '__main__':
    unittest.main()
