import os
from pathlib import Path

from .executable import Executable

###########
# FILE IO #
###########

# class SourceFile:
#     def __init__():
#         pass

class ProjectManager:
    
    # The paths have the most defined behavoir within a local directory
    # and you are running the python file within the directory
    def __init__(
        self, 
        compiler,

        extension, 
        directory, 
        
        program
    ):
        self.compiler = compiler

        self.extension = extension
        self.directory = tuple(self.validate_path(path) for path in directory)

        self.program = self.validate_path(program)
        
        # self.debug = True

    def validate_path(self, path):
        path = os.path.relpath(path)

        return path

    # generic function to traverse a directory recursively
    def traverse(self, dir, cond, action):
        for entry in os.scandir(dir):
            if entry.is_file() and cond(entry.path):
                action(entry.path)
            elif entry.is_dir():
                self.traverse(entry.path, cond, action)
    
    ################
    # SOURCE FILES #
    ################

    # get a list of all the source file paths
    def sources(self):
        files = list()

        self.traverse(
            self.directory[0], # <-- the directory of source files
            (lambda path: path.endswith(self.extension[0])), # <-- if it is a source file
            (lambda path: files.append(path)) # <-- add it to a list of source files
        )

        return files

    # creates an output path given a source file
    def source_out(self, source):
        # i think converting it to an abs path first
        # might be safer  
        source = os.path.abspath(source)

        base = os.path.splitext(source)[0]
        base = base.replace(
            os.path.abspath(self.directory[0]),
            os.path.abspath(self.directory[1]),
            1 # <-- this is just so if u mess it up somehow
        )
        base += self.extension[1]

        base = os.path.relpath(base)

        return base

    def source_cmd(self, source, args=""):
        out = str()
        out += self.compiler
        out += (" -c " + source) # <-- compile to object file
        out += (" -o " + self.source_out(source)) # <-- specify output 
        out += (" " + args + " ") # <-- add args

        return out

    def source_exc(self, source, args=""):
        return Executable.one(self.source_cmd(source, args))
    
    ################
    # PROGRAM FILE #
    ################

    def has_program(self):
        return os.path.exists(self.program)

    def program_out(self):
        # this will always be the program fil
        return os.path.splitext(self.program)[0]

    def program_cmd(self, args=""):

        if not self.has_program():
            return "echo 'Unable to find program file!'"

        # add the compiler and the path to the program
        cmd = self.compiler + " " + self.program + " " + args + " "

        # add the path to all the source files
        for source in self.sources():
            cmd += (self.source_out(source) + " ")

        # add the rest of the command
        cmd += (" -o " + self.program_out())

        return cmd

    def program_exc(self, args=""):
        return Executable.one(self.program_cmd(args))

    ###############
    # OUTPUT FILE #
    ###############

    def run_cmd(self, args=""):
        # return self.program_out() + " " + args
        return "./" + os.path.relpath(self.program_out()) + " " + args + " "

    def run_exc(self, args=""):
        return Executable.one(self.run_cmd(args))