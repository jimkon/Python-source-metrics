import argparse

from src.python.python_source_obj import PythonSourceObj


def read_args():
    parser = argparse.ArgumentParser(description='Extract stats from python codebase.')
    # https://docs.python.org/3/library/argparse.html#:~:text=in%20version%203.9.-,The%20add_argument()%20method,-%C2%B6
    parser.add_argument('src', type=str, help='Source folder')
    parser.add_argument('-d', '--dest', type=str, help="Destination exported files (stats, reports, etc...)")
    # parser.add_argument('-b', '--ex2', choices=['b1', 'b2', 'b3'], required=False, help="example required")
    # parser.add_argument('-s', '--save', action='store_false')
    # parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")

    args = vars(parser.parse_args())
    return args


def main():
    args = read_args()
    print(args)
    source = args['src']
    dest = args['dest']
    fetch_and_analyse_source(source)


def fetch_and_analyse_source(source_code_path):
    obj = PythonSourceObj(source_code_path)
    obj.print_objects()


def analyse_source(python_source_code_obj, report_dest_path):
    pass


def create_report(report_dest_path):
    pass


if __name__ == "__main__":
    main()
