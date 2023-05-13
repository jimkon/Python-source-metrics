import re


def split_camel_case_string(camel_case_string):
    """ChatGPT
    Here's how the function works:
    * The function uses the re.findall() method to find all matches of the regular expression pattern '[A-Z][a-z0-9]*|[A-Z]+' in the input class_name. This pattern matches either an uppercase letter followed by any number of lowercase letters or digits ([A-Z][a-z0-9]*), or one or more consecutive uppercase letters ([A-Z]+). The re.findall() method returns a list of all matches.
    * The function then joins the list of matches with a space separator using the join() method and returns the result.

    Here's an example usage of the function:
         _prettify_classname('MyClassName') -> 'My Class Name'
         _prettify_classname('HTTPResponse') -> 'HTTP Response'
         _prettify_classname('DB2Connection') -> 'DB2 Connection'
         _prettify_classname('MyXMLParserClass') -> 'My XML Parser Class'
         _prettify_classname('HTML') -> 'HTML'

    """
    # words = re.findall('[A-Z][a-z0-9]*|[A-Z]+', class_name) # chatGPT
    words = re.findall('.+?(?:(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', camel_case_string)
    return ' '.join(words)


def single_to_multiline_string(strings, max_length=30, seperator=', '):
    """ ChatGPT
    Takes in a list of strings and concatenates them into a multiline string with a maximum line length
    specified by `max_length`. The `seperator` parameter is used to separate the individual strings in the
    concatenated string.

    Args:
        strings (list): A list of strings to concatenate into a multiline string.
        max_length (int): The maximum length of each line in the multiline string. Defaults to 30.
        seperator (str): The string to use to separate each string in the concatenated string. Defaults to ", ".

    Returns:
        str: The concatenated multiline string.

    Example:
        >>> strings = ["This", " is a long string", "This is another long string", "Yet another long string"]
        >>> single_to_multiline_string(strings, max_length=20, seperator='; ')
        'This is a long string; \n> This is another long string; \n> Yet another long string'

    def test_create_multiline_string():
        # Test case 1: Strings fit within maximum line length
        strings = ["This is a long string", "This is another long string", "Yet another long string"]
        expected_output = "This is a long string, This is another long string, Yet another long string"
        assert _create_multiline_string(strings, max_length=30, seperator=', ') == expected_output

        # Test case 2: Strings need to be split into multiple lines
        strings = ["This is a long string", "This is another long string", "Yet another long string"]
        expected_output = "This is a long string,\n> This is another long string,\n> Yet another long string"
        assert _create_multiline_string(strings, max_length=20, seperator=', ') == expected_output

        # Test case 3: Empty list of strings
        strings = []
        expected_output = ""
        assert _create_multiline_string(strings, max_length=30, seperator=', ') == expected_output

        # Test case 4: Single string that is longer than max line length
        strings = ["This is a very long string that exceeds the maximum line length"]
        expected_output = "This is a very long string that exceeds the maximum line length"
        assert _create_multiline_string(strings, max_length=20, seperator=', ') == expected_output

        # Test case 5: Custom separator
        strings = ["This is a long string", "This is another long string", "Yet another long string"]
        expected_output = "This is a long string; \n> This is another long string; \n> Yet another long string"
        assert _create_multiline_string(strings, max_length=20, seperator='; ') == expected_output
    """
    output = ''
    current_line_length = 0

    for s in strings:
        if current_line_length + len(s) <= max_length:
            output += (seperator if len(output) > 0 else '')+s
            current_line_length += len(s)
        else:
            output += ',\n> ' + s
            current_line_length = len(s)

    return output

