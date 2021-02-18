#!/usr/bin/python

from gui.project_gui import ProgramApp
from app.manager import ProjectManager

from PyQt5 import QtWidgets

####################
# QTCLANG CLI CODE #
####################

def main():
    import sys, argparse

    parser = argparse.ArgumentParser(
        description='Create a qtclang compiler window',
        epilog='See here: https://github.com/selym3/qtclang for features, issues, updates, source code, etc.'
    )

    parser.add_argument(
        '--width',
        type=int,
        help='the width of the window',
        default=600
    )

    parser.add_argument(
        '--height',
        type=int,
        help='the height of the window',
        default=600
    )

    parser.add_argument(
        '--compiler',
        type=str,
        help='the compiler to use (default: clang++)',
        default='clang++'
    )

    parser.add_argument(
        '--in',
        dest='infile',
        type=str,
        help='the file type to compile (default: .cpp)',
        default='.cpp'
    )

    parser.add_argument(
        '--out',
        dest='outfile',
        type=str,
        help='the file type to output (default: .o)',
        default='.o'
    )

    parser.add_argument(
        '--indir',
        type=str,
        help='the directory to search for files in (default: ./src/)',
        default='./src/'
    )

    parser.add_argument(
        '--outdir',
        type=str,
        help='the directory to output files in (default: ./bin/)',
        default='./bin/'
    )

    parser.add_argument(
        '--prog',
        type=str,
        help='the program file (default: ./main.cpp)',
        default='./main.cpp'
    )

    args = parser.parse_args()

    manager = ProjectManager(
        compiler = args.compiler,

        extension = ( args.infile, args.outfile ),
        directory = ( args.indir, args.outdir ),
        
        program = args.prog
    )

    app = QtWidgets.QApplication(sys.argv)

    ex = ProgramApp(
        manager, 
        width = args.width, 
        height = args.height
    )
    ex.show()

    sys.exit(app.exec_())

TESTING = False

def test():
    import os
    print(os.getcwd())

    # import sys
    # from pathlib import Path
    # print(Path(sys.argv[0]).resolve())

if __name__ == '__main__':
    if not TESTING:
        main()
    else:
        test()