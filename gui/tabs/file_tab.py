from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from compiler import Compiler, CompilerDetails

import os

from .tab import Tab
from .component import Component

class ProjectDetails(Component):
    
    def __init__(self):
        super().__init__("Project Details")

        ### PROJECT LOCATION ###

        self.location = os.getcwd() # <-- this should be ./

        self.location_label = QLabel(self.location)
        self.addWidgets(self.location_label)

        project_location = QPushButton(f"Select Project Location")
        project_location.clicked.connect(self.update_location)
        self.addWidgets(project_location)

        ### PROGRAM LOCATION ###
        self.program = None 

        if os.path.exists('main.cpp'):
            self.program = os.path.abspath('main.cpp')
        if os.path.exists('main.c'):
            self.program = os.path.abspath('main.c')

        self.program_label = QLabel(str(self.program))
        self.addWidgets(self.program_label)

        program_location = QPushButton("Select Program File")
        program_location.clicked.connect(self.update_program)
        self.addWidgets(program_location)

    def update_location(self):
        loc = QFileDialog().getExistingDirectory(
            self,
            'Select C/C++ Project Directory',
            self.location
        )

        if loc != '':
            print("Updating location", loc)
            self.set_location(loc)
        else: 
            print("Didn't find location")

    def set_location(self, new_location):
        self.location = new_location
        self.location_label.setText(new_location)
    
    def update_program(self):
        prog, _ = QFileDialog().getOpenFileName(
            self,
            'Select C/C++ program file',
            self.location,
            'C/C++ application (*.c, *.cpp)'
        )

        if prog != '':
            print("Found:", prog)
            self.set_program(prog)
        else:
            print("Didn't find program")
    
    def set_program(self, new_program):
        self.program = new_program
        self.program_label.setText(new_program)

    def get_details(self):
        return CompilerDetails(
            self.location,
            self.program
        )

class ProjectCompiler(Component):

    def __init__(self, options_cmp, details_cmp):
        super().__init__("Compile Project")

        # Initialize references to other components
        self.options_cmp = options_cmp 
        self.details_cmp = details_cmp

        # Run button
        run_button = QPushButton("Run Program")
        run_button.clicked.connect(self.run_program)
        self.addWidgets(run_button)

        # Compile All button
        compile_button = QPushButton("Compile All")
        compile_button.clicked.connect(self.compile_all)
        self.addWidgets(compile_button)

    def get_compiler(self):
        return Compiler(
            self.options_cmp.get_options(),
            self.details_cmp.get_details()
        )

    def run_program(self): 
        compiler = self.get_compiler()
        
        compiler.compile_program()
        compiler.run_program()

    def compile_all(self):
        pass
        # compiler = self.get_compiler()
        # compiler.compile_program()

class FileTab(Tab):

    def __init__(self, parent, options_cmp):
        super().__init__(parent, "File Manager")

        project_details = ProjectDetails()
        self.addComponent(project_details)
        
        project_compiler = ProjectCompiler(options_cmp, project_details)
        self.addComponent(project_compiler)