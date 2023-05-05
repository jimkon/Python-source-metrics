import os.path
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from pystruct.objects import data_objects as do
from pystruct.utils import file_adapters


class TestSingleton(unittest.TestCase):
    """ChatGPT"""

    def test_singleton_instance(self):
        class MyClass(do.Singleton):
            pass

        # Test that two instances of MyClass are the same object
        a = MyClass()
        b = MyClass()
        self.assertIs(a, b)

    def test_singleton_subclass(self):
        class MyClass(do.Singleton):
            pass

        class MySubclass(MyClass):
            pass

        # Test that two instances of MySubclass are the same object
        a = MySubclass()
        b = MySubclass()
        self.assertIs(a, b)

    def test_multiple_subclasses(self):
        class MyClass1(do.Singleton):
            def methdod1(self):
                return 'method1'

        class MyClass2(do.Singleton):
            def methdod2(self):
                return 'method2'

        a = MyClass1()
        b = MyClass2()
        self.assertIsNot(a, b)
        self.assertEqual(a.methdod1(), 'method1')
        self.assertEqual(b.methdod2(), 'method2')

    def test_singleton_arguments(self):
        class MyClass(do.Singleton):
            def __init__(self, x, y):
                self.x = x
                self.y = y

        # Test that two instances of MyClass with different arguments are the same object
        a = MyClass(1, 2)
        self.assertEqual(a.x, 1)
        self.assertEqual(a.y, 2)
        b = MyClass(1, 3)
        self.assertIs(a, b)
        self.assertEqual(a.x, 1)
        self.assertEqual(a.y, 3)
        self.assertEqual(b.x, 1)
        self.assertEqual(b.y, 3)


class TestAbstractObject(unittest.TestCase):
    def test_data_without_file_adapter(self):
        class TestObject(do.AbstractObject):
            def __init__(self):
                super().__init__()

            def build(self):
                return 'build_result'

        obj = TestObject()
        self.assertEqual(obj.data(), 'build_result')
        self.assertEqual(obj.data(), 'build_result')

    def test_data_build_cache_and_save(self):
        class TestObject(do.AbstractObject):
            def __init__(self, file_adapter):
                super().__init__(file_adapter)

            def build(self):
                return 'build_result'

        file_adapter = MagicMock()
        file_adapter.load = MagicMock(return_value=None)
        file_adapter.save = MagicMock()

        obj = TestObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'build_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_called_once_with(obj._data)

        self.assertEqual(obj.data(), 'build_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_called_once_with(obj._data)

    def test_data_load_and_cache(self):
        class TestObject(do.AbstractObject):
            def __init__(self, file_adapter):
                super().__init__(file_adapter)

            def build(self):
                return 'build_result'

        file_adapter = MagicMock()
        file_adapter.load = MagicMock(return_value='load_result')
        file_adapter.save = MagicMock()

        obj = TestObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'load_result')
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_not_called()

        self.assertEqual(obj.data(), 'load_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_not_called()

    def test_data_load_delete_and_build(self):
        class TestObject(do.AbstractObject):
            def __init__(self, file_adapter):
                super().__init__(file_adapter)

            def build(self):
                return 'build_result'

        file_adapter = MagicMock()
        file_adapter.load = MagicMock(return_value='load_result')
        file_adapter.save = MagicMock()
        file_adapter.delete_file = MagicMock()

        obj = TestObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'load_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_not_called()

        self.assertIsNotNone(obj._data)
        obj.delete()
        file_adapter.load = MagicMock(return_value=None)
        self.assertIsNone(obj._data)
        file_adapter.delete_file.assert_called_once()

        obj = TestObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'build_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_called_once()


class TestTextObjectABC(unittest.TestCase):
    def test_lifecycle(self):
        build_result = "example_text"

        class ExampleTextObject(do.TextObjectABC):
            def __init__(self):
                super().__init__('ext')

            def build(self):
                return build_result

        obj = ExampleTextObject()
        self.assertEqual(obj.text(), build_result)
        self.assertTrue(os.path.exists(obj._file_adapter.filepath))

        del obj
        obj = ExampleTextObject()
        self.assertEqual(obj.text(), build_result)

        obj.delete()
        self.assertFalse(os.path.exists(obj._file_adapter.filepath))


class TestHTMLObjectABC(unittest.TestCase):
    def test_lifecycle(self):
        build_result = "example_html"

        class ExampleHTMLObject(do.HTMLObjectABC):
            def __init__(self):
                super().__init__()

            def build(self):
                return build_result

        obj = ExampleHTMLObject()
        self.assertEqual(obj.html(), build_result)
        self.assertTrue(os.path.exists(obj._file_adapter.filepath))

        del obj
        obj = ExampleHTMLObject()
        self.assertEqual(obj.html(), build_result)

        obj.delete()
        self.assertFalse(os.path.exists(obj._file_adapter.filepath))


class TestDataframeObjectABC(unittest.TestCase):
    def test_lifecycle(self):
        build_result = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c'],
            'col3': [True, False, None]
        })

        class ExampleDataframeObject(do.DataframeObjectABC):
            def __init__(self):
                super().__init__()

            def build(self):
                return build_result

        obj = ExampleDataframeObject()

        test_result = obj.dataframe()
        pd.testing.assert_frame_equal(test_result, build_result)
        self.assertTrue(os.path.exists(obj._file_adapter.filepath))

        del obj
        obj = ExampleDataframeObject()
        pd.testing.assert_frame_equal(obj.dataframe(), build_result)

        obj.delete()
        self.assertFalse(os.path.exists(obj._file_adapter.filepath))


class TestJSONObjectABC(unittest.TestCase):
    def test_lifecycle(self):
        build_result = [
            {'a': 0, 'b': 1},
            {'c': 2}
        ]

        class ExampleJSONObject(do.JSONObjectABC):
            def __init__(self):
                super().__init__()

            def build(self):
                return build_result

        obj = ExampleJSONObject()
        test_result = obj.json()
        self.assertEqual(test_result, build_result)
        self.assertTrue(os.path.exists(obj._file_adapter.filepath))

        del obj
        obj = ExampleJSONObject()
        self.assertEqual(obj.json(), build_result)

        obj.delete()
        self.assertFalse(os.path.exists(obj._file_adapter.filepath))


if __name__ == '__main__':
    unittest.main()
