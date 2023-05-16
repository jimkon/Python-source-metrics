import unittest

from pystruct.utils import string_utils as su


class TestSplitCamelCase(unittest.TestCase):
    def test__prettify_classname(self):
        self.assertEqual(su.split_camel_case_string('MyClassName'), 'My Class Name')
        self.assertEqual(su.split_camel_case_string('HTTPResponse'), 'HTTP Response')
        self.assertEqual(su.split_camel_case_string('DB2Connection'), 'DB2 Connection')
        self.assertEqual(su.split_camel_case_string('MyXMLParserClass'), 'My XML Parser Class')
        self.assertEqual(su.split_camel_case_string('HTML'), 'HTML')
        self.assertEqual(su.split_camel_case_string('Already split'), 'Already split')


class TestSingleToMultilineString(unittest.TestCase):
    def test_single_to_multiline_string(self):
        # Test case 1: Strings fit within maximum line length
        strings = ["This is a long string", "This is another long string", "Yet another long string"]
        expected_output = "This is a long string, This is another long string, Yet another long string"
        self.assertEqual(su.single_to_multiline_string(strings, max_length=30, seperator=', '), expected_output)

        # Test case 2: Strings need to be split into multiple lines
        strings = ["This is a long string", "This is another long string", "Yet another long string"]
        expected_output = "This is a long string;\n> This is another long string;\n> Yet another long string"
        self.assertEqual(su.single_to_multiline_string(strings, max_length=20, seperator='; '), expected_output)

        # Test case 3: Empty list of strings
        strings = []
        expected_output = ""
        self.assertEqual(su.single_to_multiline_string(strings, max_length=30, seperator=', '), expected_output)

        # Test case 4: Single string that is longer than max line length
        strings = ["This is a very long string that exceeds the maximum line length"]
        expected_output = "This is a very long string that exceeds the maximum line length"
        self.assertEqual(su.single_to_multiline_string(strings, max_length=20, seperator=', '), expected_output)

        # Test case 5: Custom separator
        strings = ["This is a long string", "This is another long string", "Yet another long string"]
        expected_output = "This is a long string;\n> This is another long string;\n> Yet another long string"
        self.assertEqual(su.single_to_multiline_string(strings, max_length=20, seperator='; '), expected_output)


if __name__ == '__main__':
    unittest.main()
