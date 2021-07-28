from pathlib import Path
import os

'''

COMPILER OPTIONS:

- which compiler to use 
- compilation flags
- program arguments

'''

class CompilerOptions:
    
    def __init__(self, compiler, flags, silenced, args=""):
        self.compiler = str(compiler)
        self.flags = str(flags)
        self.silenced = bool(silenced)
        self.args = str(args)

    def __str__(self):
        return f"{self.compiler}, {self.flags}, {self.silenced}, {self.args}"

    def __repr__(self):
        return f"CompilerOptions({self})"

DEFAULT_OPTS = CompilerOptions(
    "clang++",
    "-O3 -std=c++17 -pthread",
    True,
    ""
)

DEBUG_OPTS = CompilerOptions(
    "gcc -g",
    "-lm -pthread",
    False,
    ""
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
        compiler_options = 4
        data = []
        with open(filepath) as f:
            # this can break with an invalid file trying to be loaded
            # that is smaller than 4 lines
            while len(data) < compiler_options:
                data += [ f.readline().strip() ]
        
        return CompilerOptions(*data)

    def options_to_file(self, options):
        # when passed into bool(...) this converts properly
        is_silenced = 'Silenced' if options.silenced else ''
        
        return f"{options.compiler}\n{options.flags}\n{is_silenced}\n{options.args}"

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

        self.program = program

    def create_bin(self):
        # creates the bin folder
        Path(self.bin).mkdir(parents=True, exist_ok=True)

    def to_bin(self, path, extension):
        # moves a file specified at the path to the bin folder
        name = os.path.basename(path)
        
        # cpp must come first cause it's more complex and overlaps with 
        # the other one
        name = name\
            .replace('.cpp', extension) \
            .replace('.c', extension)
        
        return os.path.join(self.bin, name)

    def get_executable(self):
        if self.program is None: #Handle this better
            raise ValueError('Program file location is in invalid state')
        
        # converts the program file into the executable
        return self.to_bin(self.program, extension='')

    def get_source(self, path_to_source):
        #c converts the source file into object file 
        return self.to_bin(path_to_source, extension='.o')

'''

COMPILER:

- compilation for program
- compilation for source file
- command for running program

'''


def traverse(root, condition, action):
    # generic util for recursively exploring a directory

    for entry in os.scandir(root):
        if entry.is_file() and condition(entry.path):
            action(entry.path)
        elif entry.is_dir():
            traverse(entry.path, condition, action)

class Compiler:
    
    def __init__(self, options, details):
        self.options = options
        self.details = details

    def log(self, text):
        if not self.options.silenced:
            print(text)

    def _compile(self, command, with_bin=True):

        if with_bin:
            self.details.create_bin()
        
        self.log(command)
        os.system(command)

    def run_program(self):
        to_exec = self.details.get_executable() + ' ' + self.options.args
        self._compile(to_exec, with_bin=False)

    def compile_program(self):

        def bin_has_sources():
            for fd in os.scandir(self.details.bin):
                if fd.is_file() and fd.path.endswith('.o'):
                    return True
            return False

        def program_command():
            cmp = self.options.compiler 
            flg = self.options.flags

            prg = self.details.program
            exe = self.details.get_executable()

            if bin_has_sources():
                bnf = os.path.join(self.details.bin, '*.o')
            else:
                bnf = ''

            return f'{cmp} {flg} {bnf} {prg} -o {exe}'
        
        self._compile(program_command(), with_bin=True)

    def is_source_file(self, path):
        is_c_or_cpp = path.endswith('.cpp') or path.endswith('.c')
        is_program = (path == self.details.program)
        return is_c_or_cpp and not is_program

    def compile_source(self, path_to_source):
        # if self.is_source_file(path_to_source):
        #     pass

        def source_command():
            cmp = self.options.compiler
            out = self.details.get_source(path_to_source)

            return f'{cmp} -c {path_to_source} -o {out}'

        self._compile(source_command(), with_bin=True)
    
    def traverse_sources(self, action):
        traverse(
            self.details.project, #<-- project root
            self.is_source_file, #<-- if the file is a source file, do an action
            action #<-- the action to do is passed in 
        )



