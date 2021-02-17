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
        super().__init__(obj_file_compile_cmd, debug)
        self.dir_to_create = os.path.dirname(
            obj_file_compile_cmd.split(" ")[-1])

    def execute(self):
        # if self.debug:
            # print("Creating directory: " + self.dir_to_create)

        Path(self.dir_to_create).mkdir(parents=True, exist_ok=True)
        
        super(ObjExecutable, self).execute()