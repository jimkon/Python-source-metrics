def enrich_import_raw_df(df):
    df['import_root'] = df['imports'].apply(import_root)
    project_root = common_root(df['module'])
    df['is_project_module'] = df['import_root'].apply(lambda x: x == project_root)
    df['import_module'] = df['imports'].apply(lambda x: element_with_longest_match(x, df['module'].unique()))
    df['module_depth'] = df['module'].apply(lambda x: len(breakdown_import_path(x)))
    df['invalid_import'] = df['is_project_module'] & df['import_module'].isna()
    df['unused_module'] = ~df['module'].isin(df['import_module'])
    df['module_name'] = df['module'].apply(module_name)
    df['package'] = df['module'].apply(lambda x: '.'.join(breakdown_import_path(x)[:-1]))
    df['import_package'] = df['import_module'].apply(lambda x: element_with_longest_match(x, df['package'].unique()))
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

