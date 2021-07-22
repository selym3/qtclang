from pathlib import Path
import os

'''

COMPILER OPTIONS:

- which compiler to use 
- compilation flags
- program arguments

'''

class CompilerOptions:
    
    def __init__(self, compiler, flags, args=""):
        self.compiler = compiler
        self.flags = flags
        self.args = args

    def __str__(self):
        return f"{self.compiler}, {self.flags}, {self.args}"

    def __repr__(self):
        return f"CompilerOptions({self})"

DEFAULT_OPTS = CompilerOptions(
    "clang++",
    "-O3 -std=c++17 -pthread"
)

'''

COMPILER FILEIO:

- save compiler options to a file 
- read compiler options from a file

'''

class FileProtocol:
    
    def file_to_options(self, filepath):
        raise NotImplementedError(f'Method to convert contents of file "{filepath}" into instance of class CompilerOptions not implemented')

    def options_to_file(self, options):
        raise NotImplementedError(f'Method to convert {repr(options)} into the contents of a file not implemented.')
    
    def write_options(self, filename, options):
        with open(filename, 'w') as f:
            new_contents = self.options_to_file(options)
            f.write(new_contents)

class SimpleFileProtocol(FileProtocol):

    def file_to_options(self, filepath):
        data = []
        with open(filepath) as f:
            line = None
            while len(data) < 3 and line != '':
                data += [ f.readline().strip() ]
        
        return CompilerOptions(*data)

    def options_to_file(self, options):
        return f"{options.compiler}\n{options.flags}\n{options.args}"

'''

COMPILER DETAILS:

- location of the project
- location of the bin folder
- program file

'''

class CompilerDetails:
    
    def __init__(self, project, program):
        self.project = project
        self.bin = os.path. join(project, 'bin')

        if program is None: #Handle this better
            raise ValueError('Program file location is in invalid state')
        self.program = program

    def create_bin(self):
        Path(self.bin).mkdir(parents=True, exist_ok=True)

    def get_executable(self):
        prog_name = os.path.basename(self.program)
        prog_name = prog_name.replace('.cpp','').replace('.c','')

        return os.path.join(self.bin, prog_name)

'''

COMPILER:

- compilation for program
- compilation for source file
- command for running program

'''

class Compiler:
    
    def __init__(self, options, details, debug=True):
        self.options = options
        self.details = details

        self.debug = debug

    def log(self, text):
        if self.debug:
            print(text)

    def run_program(self):
        to_exec = self.details.get_executable() + ' ' + self.options.args
        self.log(to_exec)

        os.system(to_exec)

    def compile_program(self):

        def program_command():
            cmp = self.options.compiler
            flg = self.options.flags

            prg = self.details.program
            exe = self.details.get_executable()

            return f'{cmp} {flg} {prg} -o {exe}'

        self.details.create_bin()

        to_exec = program_command()
        self.log(to_exec)

        os.system(to_exec)

