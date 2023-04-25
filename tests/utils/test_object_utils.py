import abc
import unittest

from pystruct.objects import data_objects as do
from pystruct.utils import object_utils as utils


class TestObjectUtils(unittest.TestCase):
    def test_get_object_class_from_class_name(self):
        self.assertEqual(utils.get_object_class_from_class_name('AbstractObject'), do.AbstractObject)

    def test_get_all_object_classes(self):
        self.assertTrue(len(utils.get_all_object_classes()) > len(utils.get_all_concrete_object_classes()))

    def test_get_all_concrete_object_classes(self):
        concrete_objs = utils.get_all_concrete_object_classes()
        self.assertTrue(len(concrete_objs) > 0)
        for obj_classes in concrete_objs:
            self.assertNotIsInstance(obj_classes, do.AbstractObject)
            self.assertNotIsInstance(obj_classes, do.DataframeObject)
            self.assertNotIsInstance(obj_classes, do.HTMLObject)
            self.assertNotIsInstance(obj_classes, do.HTMLTableObject)


if __name__ == '__main__':
    unittest.main()
