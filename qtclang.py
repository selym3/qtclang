#!/bin/python

########################
# QTCLANG FILE IO CODE #
########################

# this is messy and needs to be updated

import os
from pathlib import Path

# Interface for executing commands
class Executable:

    def execute(self):
        pass

# An executable group 
class Executables(Executable):
    def __init__(self, executable_list):
        self.executables = executable_list
    
    def execute(self):
        for execu in self.executables:
            execu.execute()

# A simple class that takes in a string and executes it
class CmdExecutable(Executable):
    def __init__(self, command, debug=False):
        self.command = command
        self.debug = debug

    def execute(self):
        if self.debug:
            print(self.command)

        os.system(self.command)

# An executable specifically for creating object files
class ObjExecutable(CmdExecutable):
    def __init__(self, obj_file_compile_cmd, debug=False):
        super(ObjExecutable, self).__init__(obj_file_compile_cmd, debug)
        self.dir_to_create = os.path.dirname(
            obj_file_compile_cmd.split(" ")[-1])

    def execute(self):
        # if self.debug:
            # print("Creating directory: " + self.dir_to_create)

        Path(self.dir_to_create).mkdir(parents=True, exist_ok=True)
        
        super(ObjExecutable, self).execute()

# This class handles getting source paths, object paths, 
# compilation commands, program paths, and creating executin,
# 
class ProjectManager:

    # The paths have the most defined behavoir within a local directory
    # and you are running the python file within the directory
    def __init__(self, compiler, extension_in, extension_out, source_dir, output_dir, program_file_path):
        self.compiler = compiler
        self.extension = (extension_in, extension_out)
        self.source = source_dir
        self.output = output_dir
        self.program = program_file_path

        self.exec_debug = True

    def __traverse_source_files(self, dir, action):
        for entry in os.scandir(dir):
            if entry.is_file() and entry.path.endswith(self.extension[0]):
                action(entry.path)
            elif entry.is_dir():
                self.__traverse_source_files(entry.path, action)

    def __inc(self, v):
        v = v+1

    # counts source files
    def get_source_count(self):
        cnt = 0
        self.__traverse_source_files(self.source, (lambda path: self.__inc(cnt)))
        return cnt

    # get a list of all the source file paths
    def get_source_paths(self):
        source_file_names = []
        self.__traverse_source_files(
            self.source, (lambda path: source_file_names.append(path)))
        return source_file_names

    # return a path to the program file
    def get_program_path(self):
        return self.program

    # get the command text for a source file given its path
    def get_source_cmd(self, source_path, args):
        return self.compiler + " -c " + source_path + " -o " + self.get_source_output(source_path) + " " + args

    # return a list of source commands
    def get_source_cmds(self):
        output = self.get_source_paths()

        for source_path in output:
            source_path = self.get_source_cmd(source_path)

        return output

    # return a list of the object file paths
    def get_source_outputs(self):
        source_files = self.get_source_paths()

        outputs = []

        for source in source_files:
            outputs.append(self.get_source_output(source))

        return outputs

    # get an object file path given a source file path
    def get_source_output(self, source_path):
        # this replace is problematic code because it relies the source directory
        # being at the begining. If it's not, there may be a folder with an earlier
        # name and the path may be messed up entirely
        base = os.path.splitext(source_path)[0]
        base = base.replace(self.source, self.output, 1) + self.extension[1] 
        return base

    # returns the program compilation command
    def get_program_cmd(self):

        if not self.is_program_valid():
            return "echo 'Unable to find program file!'"

        # add the compiler and the path to the program
        cmd = self.compiler + " " + self.program + " "

        # add the path to all the source files
        for output in self.get_source_outputs():
            cmd += output
            cmd += " "

        # get the program path as an output path
        base = os.path.splitext(self.program)[0]

        # add the rest of the command
        cmd += (" -o " + base)

        return cmd

    # returns the program compilation command given some flags
    def get_program_cmd_with_flags(self, flags):
        if not self.is_program_valid():
            return "echo 'Unable to find program file!'"

        # add the compiler and the path to the program
        cmd = self.compiler + " " + self.program + " " + flags + " "

        # add the path to all the source files
        for output in self.get_source_outputs():
            cmd += output
            cmd += " "

        # get the program path as an output path
        base = os.path.splitext(self.program)[0]

        # add the rest of the command
        cmd += (" -o " + base)

        return cmd

    # return a list of executables representing the compilation
    # of all the source files
    def get_source_execs(self, args=""):
        output = self.get_source_paths()
        output_execs = []
        for source_path in output:
            output_execs.append(self.get_source_exec(source_path, args))

        return output_execs

    # return an executable given a source path representing its compilation
    def get_source_exec(self, source_path, args):
        return ObjExecutable(self.get_source_cmd(source_path, args), self.exec_debug)

    # get the output path of for the program file
    def get_program_output(self, args=""):
        return os.path.splitext(self.program)[0] + " " + args

    # get the executable object for a program file, representing its compilation
    def get_program_exec(self):
        return CmdExecutable(self.get_program_cmd(), self.exec_debug)

    # get the executable object for a program file with some flags
    def get_program_exec_with_flags(self, flags):
        return CmdExecutable(self.get_program_cmd_with_flags(flags), self.exec_debug)

    # check if the program file exists
    def is_program_valid(self):
        return os.path.exists(self.program)


####################
# QTCLANG GUI CODE #
####################

# this code is less bad than the executable code

from PyQt5 import QtWidgets

class ProgramApp(QtWidgets.QWidget):
    def __init__(self, program_manager, width, height):
        super(ProgramApp, self).__init__()
        self.setFixedSize(width, height)
        self.manager = program_manager
        self.setWindowTitle("qtclang")

        # Create root form layout
        self.root = QtWidgets.QFormLayout()

        # Assign important components
        self.args_box = QtWidgets.QLineEdit()
        self.flags_box = QtWidgets.QLineEdit()
        self.src_flags_box = QtWidgets.QLineEdit()

        # Add all sub components
        self.root.addRow(self.get_config_area())

        # get the rows before the the source is added
        self.rows_before = self.root.rowCount()
        self.root.addRow(self.get_source_area())

        # Add root layout to window
        self.setLayout(self.root)

    ###
    # CONFIGURATION AREA CODE
    ##

    def get_config_area(self):
        
        options_box = QtWidgets.QGroupBox('Options')
        layout = QtWidgets.QFormLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(options_box)
        scroll_area.setWidgetResizable(True)

        ### ADD BUTTONS HERE ###

        layout.addRow(
            QtWidgets.QLabel('Program arguments: '),
            self.args_box
        )

        layout.addRow(
            QtWidgets.QLabel('Program compilation flags: '),
            self.flags_box
        )

        layout.addRow(
            QtWidgets.QLabel('Source file compilation flags: '),
            self.src_flags_box
        )

        run_button = QtWidgets.QPushButton('Run Program')
        run_button.clicked.connect(
            lambda: CmdExecutable("./" + self.manager.get_program_output(self.get_args())).execute()
        )
        layout.addRow(run_button)

        compile_button = QtWidgets.QPushButton('Compile Program')
        compile_button.clicked.connect(
            lambda: self.manager.get_program_exec_with_flags(self.get_flags()).execute()
        )
        layout.addRow(compile_button)

        compile_all = QtWidgets.QPushButton('Compile All Sources')
        compile_all.clicked.connect(
            lambda: Executables(self.manager.get_source_execs(self.get_src_flags())).execute()
        )
        layout.addRow(compile_all)

        refresh = QtWidgets.QPushButton('Refresh sources')
        refresh.clicked.connect(
            lambda: self.refresh_sources()
        )
        layout.addRow(refresh)

        ########################

        options_box.setLayout(layout)

        return scroll_area

    def get_args(self):
        return self.args_box.text()

    def get_src_flags(self):
        return self.src_flags_box.text()

    def get_flags(self):
        return self.flags_box.text()

    ###
    # SOURCE AREA CODE
    ###

    def get_source_area(self):
        
        source_box = QtWidgets.QGroupBox('Sources')
        layout = QtWidgets.QFormLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(source_box)
        scroll_area.setWidgetResizable(True)

        for source in self.manager.get_source_paths():
            self.add_source(layout, source)

        source_box.setLayout(layout)

        return scroll_area

    def add_source(self, layout, source):
        out = self.manager.get_source_output(source)

        title = QtWidgets.QLabel(source)
        button = QtWidgets.QPushButton('Compile Source (' + out + ')')

        button.clicked.connect(lambda: self.manager.get_source_exec(source, self.get_src_flags()).execute())

        layout.addRow(title, button)

    def refresh_sources(self):
        if self.root.rowCount() == self.rows_before + 1:
            self.root.removeRow(self.rows_before)

        self.root.addRow(self.get_source_area())

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