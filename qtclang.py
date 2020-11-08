from PyQt5 import QtWidgets
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
    def get_source_cmd(self, source_path):
        return self.compiler + " -c " + source_path + " -o " + self.get_source_output(source_path)

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
    def get_source_execs(self):
        output = self.get_source_paths()
        output_execs = []
        for source_path in output:
            output_execs.append(self.get_source_exec(source_path))

        return output_execs

    # return an executable given a source path representing its compilation
    def get_source_exec(self, source_path):
        return ObjExecutable(self.get_source_cmd(source_path), self.exec_debug)

    # get the output path of for the program file
    def get_program_output(self):
        return os.path.splitext(self.program)[0]

    # get the executable object for a program file, representing its compilation
    def get_program_exec(self):
        return CmdExecutable(self.get_program_cmd(), self.exec_debug)

    # get the executable object for a program file with some flags
    def get_program_exec_with_flags(self, flags):
        return CmdExecutable(self.get_program_cmd_with_flags(flags), self.exec_debug)

    # check if the program file exists
    def is_program_valid(self):
        return os.path.exists(self.program)

class ProgramApp(QtWidgets.QWidget):
    def __init__(self, program_manager, width, height):
        super(ProgramApp, self).__init__()
        self.setFixedSize(width, height)
        self.manager = program_manager

        self.layout = QtWidgets.QFormLayout()

        # Refresh button
        refresh_button = QtWidgets.QPushButton('Refresh Sources')
        refresh_button.clicked.connect(lambda: self.__setup_sources())
        # Flag text
        self.flags_box = QtWidgets.QLineEdit()

        self.layout.addRow(refresh_button, self.flags_box)

        # Run button
        run_button = QtWidgets.QPushButton('Run Program')
        run_button.clicked.connect(lambda: CmdExecutable("./" + program_manager.get_program_output()).execute())

        # compile all button
        compile_all = QtWidgets.QPushButton('Compile All Sources')
        compile_all.clicked.connect(lambda: Executables(program_manager.get_source_execs()).execute() )

        self.layout.addRow(run_button, compile_all)

        # Program title 
        p_title = QtWidgets.QLabel(program_manager.program)
        
        # Program button
        p_button = QtWidgets.QPushButton('Compile Program')
        p_button.clicked.connect(
            lambda: program_manager.get_program_exec_with_flags(self.__get_flags()).execute()
        )

        self.layout.addRow(p_title, p_button)

        self.__setup_sources()

        self.setLayout(self.layout)
        self.setWindowTitle("qtclang")

    def __get_flags(self):
        return self.flags_box.text()

    def __setup_sources(self):
        if self.layout.rowCount() == 4:
            self.layout.removeRow(3)
        
        source_box = QtWidgets.QGroupBox('Sources')
        
        source_box_layout = QtWidgets.QFormLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(source_box)
        scroll_area.setWidgetResizable(True)

        source_box.setLayout(source_box_layout)

        for source in self.manager.get_source_paths():
            self.__add(source_box_layout, source)

        self.layout.addRow(scroll_area)

    def __add(self, layout, source):
        out = self.manager.get_source_output(source)
        ex = self.manager.get_source_exec(source)

        title = QtWidgets.QLabel(source)
        button = QtWidgets.QPushButton('Compile Source (' + out + ')')

        button.clicked.connect(lambda: ex.execute())

        layout.addRow(title, button)

def main():
    import sys

    manager = ProjectManager(
        compiler="clang++",
        extension_in=".cpp",
        extension_out=".o",
        source_dir="./src/",
        output_dir="./bin/",
        program_file_path="./main.cpp"
    )

    app = QtWidgets.QApplication(sys.argv)
    ex = ProgramApp(
        manager, 
        width=600, 
        height=600
    )

    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()