import unittest
from unittest.mock import patch, MagicMock

from src.objects.data_objects import AbstractObject


class TestAbstractObject(unittest.TestCase):
    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, 'build', return_value='build_ret')
    def test_data_without_file_strategy(self, mock_build):
        obj = AbstractObject()
        self.assertEqual(obj.data(), 'build_ret')
        mock_build.assert_called_once()

    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, 'build', return_value='build_ret')
    def test_data_build_save_cache(self, mock_build):
        file_strategy = MagicMock()
        file_strategy.load = MagicMock(return_value=None)
        file_strategy.save = MagicMock()

        obj = AbstractObject(file_strategy)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'build_ret')
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_called_once()
        mock_build.assert_called_once()

        self.assertEqual(obj.data(), 'build_ret')
        self.assertIsNotNone(obj._data)
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_called_once()
        mock_build.assert_called_once()

    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, 'build', return_value='build_ret')
    def test_data_save_cache(self, mock_build):
        file_strategy = MagicMock()
        file_strategy.load = MagicMock(return_value='load_ret')
        file_strategy.save = MagicMock()

        obj = AbstractObject(file_strategy)
        self.assertIsNone(obj._data)
        self.assertEqual(obj.data(), 'load_ret')
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_not_called()
        mock_build.assert_not_called()

        self.assertEqual(obj.data(), 'load_ret')
        self.assertIsNotNone(obj._data)
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_not_called()
        mock_build.assert_not_called()


if __name__ == '__main__':
    unittest.main()
