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
        dest='in_file_type',
        type=str,
        help='the file type to compile (default: .cpp)',
        default='.cpp'
    )

    parser.add_argument(
        '--out',
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
        compiler=args.compiler,
        extension_in=args.in_file_type,
        extension_out=args.out,
        source_dir=args.indir,
        output_dir=args.outdir,
        program_file_path=args.prog
    )

    app = QtWidgets.QApplication(sys.argv)
    ex = ProgramApp(
        manager, 
        width=args.width, 
        height=args.height
    )

    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()