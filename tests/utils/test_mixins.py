import unittest

from pystruct.utils import mixins as mx

class TestPrettifiedClassNameMixin(unittest.TestCase):
    def test__prettify_classname(self):
        self.assertEqual(mx.PrettifiedClassNameMixin._prettify_classname('MyClassName'), 'My Class Name')
        self.assertEqual(mx.PrettifiedClassNameMixin._prettify_classname('HTTPResponse'), 'HTTP Response')
        self.assertEqual(mx.PrettifiedClassNameMixin._prettify_classname('DB2Connection'), 'DB2 Connection')
        self.assertEqual(mx.PrettifiedClassNameMixin._prettify_classname('MyXMLParserClass'), 'My XML Parser Class')
        self.assertEqual(mx.PrettifiedClassNameMixin._prettify_classname('HTML'), 'HTML')


if __name__ == '__main__':
    unittest.main()
