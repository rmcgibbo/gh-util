import sys
import argparse
from . import main_login
from . import main_list_prs

def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    p = argparse.ArgumentParser()
    sub_parsers = p.add_subparsers(metavar='command', dest='cmd')

    main_login.configure_parser(sub_parsers)
    main_list_prs.configure_parser(sub_parsers)

    args = p.parse_args()
    args_func(args, p)

def args_func(args, p):
    try:
        args.func(args, p)
    except Exception as e:
        if e.__class__.__name__ not in ('ScannerError', 'ParserError'):
            message = """\
An unexpected error has occurred, please consider sending the
following traceback to the conda GitHub issue tracker at:
    https://github.com/rmcgibbo/gh-util/issues
Include the output of the command 'conda info' in your report.
"""
            print(message)
        raise  # as if we did not catch it

if __name__ == '__main__':
    main()
