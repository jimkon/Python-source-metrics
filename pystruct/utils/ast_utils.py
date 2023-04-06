import ast

from pystruct.utils.logs import log_yellow


class MissMatchSizeBetweenAstAndCodeSegment(ValueError):
    pass


class InvalidSubclassType(ValueError):
    pass


def analyse_ast(code_segment):
    try:
        return list(ast.walk(ast.parse(code_segment, mode='exec')))
    except SyntaxError:
        log_yellow(f"Warning-> Unable to analyse the syntax of code segment:\n\"{code_segment}\"", verbosity=3)
        return []


def remove_first_n_characters(code_lines, offset):
    return [code_line[offset:] for code_line in code_lines]


def separate_statement(code, ast_var):
    if not issubclass(ast_var.__class__, ast.stmt):
        raise InvalidSubclassType(f"Type of ast_var must be a subclass of ast.stmt type.")

    start_lineno, end_lineno, col_offest = ast_var.lineno, ast_var.end_lineno, ast_var.col_offset

    start_lineno -= len(ast_var.decorator_list)

    code_lines = code.split('\n')

    if start_lineno < 0 or end_lineno > len(code_lines):
        raise MissMatchSizeBetweenAstAndCodeSegment(f"Incorrect line numbers. Trying to fetch lines {start_lineno=} and {end_lineno=} code from {code=}.")

    code_segment = code_lines[start_lineno-1:end_lineno]
    res_code_str = '\n'.join(remove_first_n_characters(code_segment, col_offest))

    remaining_code_lines = code_lines[:start_lineno-1]
    remaining_code_lines.extend(code_lines[end_lineno:])
    remaining_code_lines_str = '\n'.join(remaining_code_lines)

    return res_code_str, remaining_code_lines_str


def get_first_ast_of_type(code, list_of_types):# todo maybe avoid calling analyse_ast
    asts = analyse_ast(code)
    for _ast in asts:
        for _type in list_of_types:
            if isinstance(_ast, _type):
                return _ast
    return None


def fetch_compound_statement(asts_to_fetch, from_code):
    fetched_ast = get_first_ast_of_type(from_code, asts_to_fetch)

    if not fetched_ast:
        return None, from_code
    else:
        fetched_code, remaining_code = separate_statement(from_code, fetched_ast)
        return fetched_code, fetched_ast, remaining_code
