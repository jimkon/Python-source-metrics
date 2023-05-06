import unittest

from pystruct.utils.string_utils import split_camel_case_string


class TestSplitCamelCase(unittest.TestCase):
    def test__prettify_classname(self):
        self.assertEqual(split_camel_case_string('MyClassName'), 'My Class Name')
        self.assertEqual(split_camel_case_string('HTTPResponse'), 'HTTP Response')
        self.assertEqual(split_camel_case_string('DB2Connection'), 'DB2 Connection')
        self.assertEqual(split_camel_case_string('MyXMLParserClass'), 'My XML Parser Class')
        self.assertEqual(split_camel_case_string('HTML'), 'HTML')
        self.assertEqual(split_camel_case_string('Already split'), 'Already split')


if __name__ == '__main__':
    unittest.main()
