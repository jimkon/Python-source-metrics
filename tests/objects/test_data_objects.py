import unittest
from unittest.mock import patch, MagicMock

from pystruct.objects import data_objects as do


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
    @patch.multiple(do.AbstractObject, __abstractmethods__=set())
    @patch.object(do.AbstractObject, 'build', return_value='build_result')
    def test_data_without_file_adapter(self, mock_build):
        obj = do.AbstractObject()
        self.assertEqual(obj.data(), 'build_result')
        self.assertEqual(obj.data(), 'build_result')
        mock_build.assert_called_once()

    @patch.multiple(do.AbstractObject, __abstractmethods__=set())
    @patch.object(do.AbstractObject, 'build', return_value='build_result')
    def test_data_build_cache_and_save(self, mock_build):
        file_adapter = MagicMock()
        file_adapter.load = MagicMock(return_value=None)
        file_adapter.save = MagicMock()

        obj = do.AbstractObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'build_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_called_once_with(obj._data)
        mock_build.assert_called_once()

        self.assertEqual(obj.data(), 'build_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_called_once_with(obj._data)
        mock_build.assert_called_once()

    @patch.multiple(do.AbstractObject, __abstractmethods__=set())
    @patch.object(do.AbstractObject, 'build', return_value='build_result')
    def test_data_load_and_cache(self, mock_build):
        file_adapter = MagicMock()
        file_adapter.load = MagicMock(return_value='load_result')
        file_adapter.save = MagicMock()

        obj = do.AbstractObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'load_result')
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_not_called()
        mock_build.assert_not_called()

        self.assertEqual(obj.data(), 'load_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_not_called()
        mock_build.assert_not_called()

    @patch.multiple(do.AbstractObject, __abstractmethods__=set())
    @patch.object(do.AbstractObject, 'build', return_value='build_result')
    def test_data_load_delete_and_build(self, mock_build):
        file_adapter = MagicMock()
        file_adapter.load = MagicMock(return_value='load_result')
        file_adapter.save = MagicMock()
        file_adapter.delete_file = MagicMock()

        obj = do.AbstractObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'load_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_not_called()
        mock_build.assert_not_called()

        self.assertIsNotNone(obj._data)
        obj.delete()
        file_adapter.load = MagicMock(return_value=None)
        self.assertIsNone(obj._data)
        file_adapter.delete_file.assert_called_once()

        obj = do.AbstractObject(file_adapter)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'build_result')
        self.assertIsNotNone(obj._data)
        file_adapter.load.assert_called_once()
        file_adapter.save.assert_called_once()
        mock_build.assert_called_once()


if __name__ == '__main__':
    unittest.main()
