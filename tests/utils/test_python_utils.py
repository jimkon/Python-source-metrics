import unittest
from unittest.mock import patch

from pystruct.utils import python_utils


class TestSingleton(unittest.TestCase):
    """ChatGPT"""

    def test_singleton_instance(self):
        class MyClass(python_utils.Singleton):
            pass

        # Test that two instances of MyClass are the same object
        a = MyClass()
        b = MyClass()
        self.assertIs(a, b)

    def test_singleton_subclass(self):
        class MyClass(python_utils.Singleton):
            pass

        class MySubclass(MyClass):
            pass

        # Test that two instances of MySubclass are the same object
        a = MySubclass()
        b = MySubclass()
        self.assertIs(a, b)

    def test_multiple_subclasses(self):
        class MyClass1(python_utils.Singleton):
            def methdod1(self):
                return 'method1'

        class MyClass2(python_utils.Singleton):
            def methdod2(self):
                return 'method2'

        a = MyClass1()
        b = MyClass2()
        self.assertIsNot(a, b)
        self.assertEqual(a.methdod1(), 'method1')
        self.assertEqual(b.methdod2(), 'method2')

    def test_singleton_arguments(self):
        class MyClass(python_utils.Singleton):
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


class TestMultiSingleton(unittest.TestCase):
    def test_single_instance_creation(self):
        # Test that a single instance is created for a specific key
        instance1 = python_utils.MultiSingleton('key1')
        instance2 = python_utils.MultiSingleton('key1')
        self.assertEqual(instance1, instance2)

    def test_multiple_instance_creation(self):
        # Test that multiple instances are not created for different keys
        instance1 = python_utils.MultiSingleton('key1')
        instance2 = python_utils.MultiSingleton('key2')
        self.assertNotEqual(instance1, instance2)

    def test_existing_instance_retrieval(self):
        # Test that an existing instance is retrieved for a specific key
        instance1 = python_utils.MultiSingleton('key1')
        instance2 = python_utils.MultiSingleton('key1')
        instance3 = python_utils.MultiSingleton('key2')
        instance4 = python_utils.MultiSingleton('key2')
        self.assertEqual(instance1, instance2)
        self.assertEqual(instance3, instance4)
        self.assertNotEqual(instance1, instance3)


if __name__ == '__main__':
    unittest.main()
