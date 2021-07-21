from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os

from .tab import Tab
from .component import Component

class ProjectDetails(Component):
    
    def __init__(self):
        super().__init__("Project Details")

        ### PROJECT LOCATION

        self.location = os.getcwd() # <-- this should be ./

        self.location_label = QLabel(self.location)
        self.addWidgets(self.location_label)

        project_location = QPushButton(f"Select Project Location")
        project_location.clicked.connect(self.update_location)
        self.addWidgets(project_location)

        ### BIN FOLDER 

        self.bin = os.path.join(os.getcwd(), 'bin')

        self.bin_label = QLabel(self.bin)
        self.addWidgets(self.bin_label)

        bin_location = QPushButton("Select Output Folder")
        bin_location.clicked.connect(self.update_bin)
        self.addWidgets(bin_location)

        ### PROGRAM LOCATION 

        self.program = None

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

    def update_bin(self):
        loc = QFileDialog().getExistingDirectory(
            self,
            'Select C/C++ Project Output Directory',
            self.location
        )

        if loc != '':
            print("Updating bin location", loc)
            self.bin = loc
            self.bin_label.setText(self.bin)
        else:
            print("Didn't find bin folder")

class ProjectCompiler(Component):

    def __init__(self):
        super().__init__("Compile Project")

        # Run button
        run_button = QPushButton("Run Program")
        run_button.clicked.connect(self.run_program)
        self.addWidgets(run_button)

        # Compile All button
        compile_button = QPushButton("Compile All")
        compile_button.clicked.connect(self.compile_all)
        self.addWidgets(compile_button)

    def run_program(self): 
        pass 

    def compile_all(self):
        pass



class FileTab(Tab):

    def __init__(self, parent):
        super().__init__(parent, "File Manager")

        project_details = ProjectDetails()
        self.addComponent(project_details)
        
        project_compiler = ProjectCompiler()
        self.addComponent(project_compiler)