import unittest
from unittest.mock import patch, MagicMock

from pystruct.objects.data_objects import AbstractObject


class TestAbstractObject(unittest.TestCase):
    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, 'build', return_value='build_ret')
    def test_data_without_file_strategy(self, mock_build):
        obj = AbstractObject()
        self.assertEqual(obj._prepare_data(), 'build_ret')
        mock_build.assert_called_once()

    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, 'build', return_value='build_ret')
    def test_data_build_save_cache(self, mock_build):
        file_strategy = MagicMock()
        file_strategy.load = MagicMock(return_value=None)
        file_strategy.save = MagicMock()

        obj = AbstractObject(file_strategy)
        self.assertIsNone(obj._data)
        self.assertEqual(obj._prepare_data(), 'build_ret')
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_called_once_with(obj._data)
        mock_build.assert_called_once()

        self.assertEqual(obj._prepare_data(), 'build_ret')
        self.assertIsNotNone(obj._data)
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_called_once_with(obj._data)
        mock_build.assert_called_once()

    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, 'build', return_value='build_ret')
    def test_data_save_cache(self, mock_build):
        file_strategy = MagicMock()
        file_strategy.load = MagicMock(return_value='load_ret')
        file_strategy.save = MagicMock()

        obj = AbstractObject(file_strategy)
        self.assertIsNone(obj._data)
        self.assertEqual(obj._prepare_data(), 'load_ret')
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_not_called()
        mock_build.assert_not_called()

        self.assertEqual(obj._prepare_data(), 'load_ret')
        self.assertIsNotNone(obj._data)
        file_strategy.load.assert_called_once()
        file_strategy.save.assert_not_called()
        mock_build.assert_not_called()

    @patch.multiple(AbstractObject, __abstractmethods__=set())
    @patch.object(AbstractObject, '_prepare_data', side_effect=Exception)
    def test_data(self, *args):
        self.assertIsNotNone(AbstractObject().data())


if __name__ == '__main__':
    unittest.main()
