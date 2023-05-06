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
