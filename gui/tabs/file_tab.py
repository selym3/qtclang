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
    
    def update_program(self, was_missing=False):
        if was_missing:
            dialog_name = 'C/C++ program is missing, please select'
        else:
            dialog_name = 'Select C/C++ program file'

        prog, _ = QFileDialog().getOpenFileName(
            self,
            dialog_name,
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

class CompilerComponent(Component):

    def __init__(self, name, options_component, details_component):
        super().__init__(name)

        self.options_component = options_component
        self.details_component = details_component

    def get_options(self):
        return self.options_component.get_options()        

    def get_details(self):
        return self.details_component.get_details()

    def get_compiler(self):
        return Compiler(
            self.get_options(),
            self.get_details()
        )

class ProjectCompiler(CompilerComponent):

    def __init__(self, options_cmp, details_cmp):
        super().__init__("Compile Project", options_cmp, details_cmp)

        # Run button
        run_button = QPushButton("Run Program")
        run_button.clicked.connect(self.run_program)
        self.addWidgets(run_button)

        # Compile All button
        compile_button = QPushButton("Compile All")
        compile_button.clicked.connect(self.compile_all)
        self.addWidgets(compile_button)

    def run_program(self): 
        try:
            compiler = self.get_compiler()

            compiler.compile_program()
            compiler.run_program()
        # except InvalidCompilerState as e:
        except ValueError as e:
            self.details_component.update_program(was_missing=True)


    def compile_all(self):
        compiler = self.get_compiler()
        compiler.traverse_sources(compiler.compile_source)

class FileCompiler(CompilerComponent):
    
    def __init__(self, options_cmp, details_cmp):
        super().__init__("File Menu", options_cmp, details_cmp)
        
        refresh_btn = QPushButton("Refresh Sources")
        refresh_btn.clicked.connect(self.refresh_sources)
        self.addWidgets(refresh_btn)

        self.load_files()
    
    def load_files(self):
        compiler = self.get_compiler()
        compiler.traverse_sources(self.add_source_file)

    def refresh_sources(self):
        # - this is kinda hacky
        # - starting at 1 avoids teh refresh button
        while self.form.count() > 1:
            self.form.removeRow(1)

        self.load_files()

    def add_source_file(self, path):
        source_btn = QPushButton(f"Compile {os.path.basename(path)}")
        source_btn.clicked.connect(lambda: self.get_compiler().compile_source(path))
        self.addWidgets(source_btn)


class FileTab(Tab):

    def __init__(self, parent, options_cmp):
        super().__init__(parent, "File Manager")

        project_details = ProjectDetails()
        self.addComponent(project_details)
        
        project_compiler = ProjectCompiler(options_cmp, project_details)
        self.addComponent(project_compiler)

        file_compiler = FileCompiler(options_cmp, project_details)
        self.addComponent(file_compiler)