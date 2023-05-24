from pystruct.utils.python_utils import is_python_builtin_package


def enrich_import_raw_df(df):
    # takes an imported path e.x "a.b.c" and keeps only the first component "a"
    df['import_root'] = df['imports'].apply(import_root)

    # if no-imports
    df['is_no_imports'] = df['import_root'] == 'no-imports'

    # finds the root path of all the module paths
    project_root = common_root(df['module'])

    # checks if it is an internal/in-project module
    df['is_internal'] = df['import_root'].apply(lambda x: x == project_root)

    # checks if it is an external/3rd-party python library
    df['is_external'] = ~df['is_internal'] & ~df['is_no_imports']

    # checks if it is a python built-in module
    df['is_builtin'] = df['imports'].apply(is_python_builtin_package)

    # finds the module import path for in-project imports
    df['import_module'] = df['imports'].apply(lambda x: element_with_longest_match(x, df['module'].unique()))

    # calculate the depth of a module path
    df['module_depth'] = df['module'].apply(lambda x: len(breakdown_import_path(x)))

    # check if imported in-project module exists and therefore if it is an valid import path
    df['invalid_import'] = df['is_internal'] & df['import_module'].isna()

    # check if a module is imported anywhere in the project
    df['unused_module'] = ~df['module'].isin(df['import_module'])

    # keeps only the name of the module ex "a.b.c" -> "c"
    df['module_name'] = df['module'].apply(module_name)

    # finds the package path of each module
    df['package'] = df['module'].apply(lambda x: '.'.join(breakdown_import_path(x)[:-1]))

    # short package name ex a.b.c -> c
    df['package_name'] = df['package'].apply(lambda x: breakdown_import_path(x)[-1])

    # finds the package path of each in-project import
    df['import_package_temp'] = df['import_module'].apply(lambda x: element_with_longest_match(x, df['package'].unique()))

    # similar to import_package_temp column but for com packages too
    df['import_package'] = df.apply(lambda row: row['import_package_temp'] if row['is_internal'] else row['import_root'], axis=1)
    del df['import_package_temp']

    df['is_init_file'] = df['module_name'] == '__init__'

    return df


def breakdown_import_path(import_path):
    return import_path.split('.')


def import_root(import_path):
    return breakdown_import_path(import_path)[0]


def module_name(module_path):
    return breakdown_import_path(module_path)[-1]


def common_root(module_paths):
    roots = module_paths.apply(import_root)
    vc = roots.value_counts()
    if len(vc) != 1:
        raise ValueError(f"Module paths don't all have the same root: {vc}")
    return vc.index[0]


def element_with_longest_match(string, list_of_strings):
    if not string:
        return None

    longest_match_len = -1
    longest_match_element = None
    for element in list_of_strings:
        if string.startswith(element):
            match_len_inv = len(string.replace(element, ''))
            if longest_match_len == -1 or match_len_inv < longest_match_len:
                longest_match_len = match_len_inv
                longest_match_element = element
    return longest_match_element

