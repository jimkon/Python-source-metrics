def write_text_to_file(filepath, data):
    with open(filepath, 'w') as fp:
        fp.write(data)


def read_text_from_file(filepath):
    with open(filepath, 'r') as fp:
        return fp.read()
