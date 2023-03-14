import argparse

from pystruct.objects.full_report import FullReport
from pystruct.objects.grab_code import grab_code
from pystruct.python.python_source_obj import PythonSourceObj


def read_args():
    parser = argparse.ArgumentParser(description='Extract stats from python codebase.')
    # https://docs.python.org/3/library/argparse.html#:~:text=in%20version%203.9.-,The%20add_argument()%20method,-%C2%B6
    parser.add_argument('pystruct', type=str, help='Source folder')
    # parser.add_argument('-d', '--dest', type=str, help="Destination exported files (stats, reports, etc...)")
    # parser.add_argument('-b', '--ex2', choices=['b1', 'b2', 'b3'], required=False, help="example required")
    # parser.add_argument('-s', '--save', action='store_false')
    # parser.add_argument("-v", "--verbosity", action="count", default=0, help="increase output verbosity")

    args = vars(parser.parse_args())
    return args


def main():
    args = read_args()
    print(args)
    source = args['pystruct']

    grab_code(source)

    FullReport().data()


def fetch_and_analyse_source(source_code_path):
    obj = PythonSourceObj(source_code_path)


if __name__ == "__main__":
    main()
