from PyQt5.QtWidgets import * # QScrollArea, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *

import os

from compiler import CompilerOptions, DEBUG_OPTS, SimpleFileProtocol, traverse, DEFAULT_OPTS

from .tab import Tab
from .component import Component

class OptionsEditor(Component):

    def __init__(self):
        super().__init__("Options")

        self.compiler_input = QLineEdit()
        self.addWidgets(QLabel("Compiler: "), self.compiler_input)

        self.flags_input = QLineEdit()
        self.addWidgets(QLabel("Flags: "), self.flags_input)

        self.args_input = QLineEdit()
        self.addWidgets(QLabel("Args: "), self.args_input)

        self.debug_toggle = QCheckBox("Silence Compiler Output?")
        self.addWidgets(self.debug_toggle)

    def load_options(self, options):
        self.compiler_input.setText(options.compiler)
        self.flags_input.setText(options.flags)
        self.debug_toggle.setChecked(options.silenced)
        self.args_input.setText(options.args)
    
    def get_options(self): 
        return CompilerOptions(
            self.compiler_input.text(),
            self.flags_input.text(),
            self.debug_toggle.isChecked(),
            self.args_input.text()
        )

class SaveMenu(Component):

    def __init__(self, editor, file_converter):
        super().__init__("Save / Load")
        self.editor = editor

        self.file_converter = file_converter

        load_file = QPushButton("Load Configuration")
        load_file.clicked.connect(self.load_save_file)
        self.addWidgets(load_file)

        save_file = QPushButton("Save Configuration")
        save_file.clicked.connect(self.save_options)
        self.addWidgets(save_file)

    def load_save_file(self):
        fname, _ = QFileDialog().getOpenFileName(
            self, 
            'Select Configuration File', # <-- file dialog name 
            '', # <-- directory to start file exploraton from
            "qtclang configuration (*.qtclang)" # <-- filter
        )
        
        if fname != '':
            options = self.file_converter.file_to_options(fname)
            self.editor.load_options(options)
        else:
            print("Didn't find file to load")

    def save_options(self):
        fname, _ = QFileDialog().getSaveFileName(
            self,
            'Select Configuration File',
            '',
            'qtclang configuration (*.qtclang)' 
        )

        print("Saving file", fname)
        if fname != '':
            if not fname.endswith('.qtclang'):
                fname += '.qtclang'

            self.file_converter.write_options(fname, self.editor.get_options())
        else:
            print("Didn't find file")

class PresetSelector(Component):

    def __init__(self, editor, presets, file_converter):
        super().__init__("Presets")

        self.editor = editor
        self.file_converter = file_converter

        for name, compiler_opts in presets:
            self.add_preset(name, compiler_opts)

        traverse(
            # this should technically be from the project directory
            # but they dont know about each other
            os.getcwd(), 
            
            lambda path: path.endswith('.qtclang'),
            self.load_preset
        )

    def load_preset(self, path):
        options = self.file_converter.file_to_options(path)
        path = os.path.basename(path)

        self.add_preset(path, options)

    def add_preset(self, name, opts):
        button = QPushButton(name)
        button.clicked.connect(lambda: self.editor.load_options(opts))

        self.addWidgets(button)
        

class CompilerTab(Tab):

    def __init__(self, parent):
        super().__init__(parent, "Compiler")

        editor = OptionsEditor()
        editor.load_options(DEFAULT_OPTS)
        self.addComponent(editor)

        file_converter = SimpleFileProtocol()
        save_menu = SaveMenu(editor, file_converter)
        self.addComponent(save_menu)

        presets = [
            ("Default", DEFAULT_OPTS),
            ("Debug", DEBUG_OPTS)
        ]
        preset_selector = PresetSelector(editor, presets, file_converter)
        self.addComponent(preset_selector)

        self.options = editor

    # def get_options(self):
    #     return self.editor.get_options()