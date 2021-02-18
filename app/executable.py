# this is messy and needs to be updated

import os
from pathlib import Path

# Interface for executing commands
class Executable:
    
    ################
    # CONSTRUCTORS #
    ################

    def one(command):
        return Executable([ command ])

    def many(commands):
        return Executable(commands)

    #########
    # CLASS #
    #########

    def __init__(self, commands):
        self.commands = commands
        self.prefix = ">"

    def execute(self, debug=True):

        self.output(self.prefix * 16, debug)

        for command in self.commands:
            self.output(self.format(command), debug)

            os.system(command)
        
        self.output(self.prefix * 16, debug)

    #################
    # DEBUG OPTIONS #
    #################

    def format(self, text):
        return self.prefix + " " + str(text)

    def output(self, text, debug):
        if debug:
            print(text)

    def set_debug(self, new_debug):
        self.debug = new_debug
        return self