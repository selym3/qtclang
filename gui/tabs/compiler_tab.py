from PyQt5.QtWidgets import * # QScrollArea, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *

from compiler import CompilerOptions, SimpleFileProtocol, DEFAULT_OPTS

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

    def __init__(self, editor):
        super().__init__("Save / Load")
        self.editor = editor

        self.file_converter = SimpleFileProtocol()

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

    def __init__(self, editor, presets):
        super().__init__("Presets")

        for name, compiler_opts in presets:
            button = QPushButton(name)
            button.clicked.connect(lambda: editor.load_options(compiler_opts))

            self.addWidgets(button)

class CompilerTab(Tab):

    def __init__(self, parent):
        super().__init__(parent, "Compiler")

        editor = OptionsEditor()
        editor.load_options(DEFAULT_OPTS)
        self.addComponent(editor)

        save_menu = SaveMenu(editor)
        self.addComponent(save_menu)

        presets = [
            ("Default", DEFAULT_OPTS),
        ] * 3
        preset_selector = PresetSelector(editor, presets)
        self.addComponent(preset_selector)

        self.options = editor

    # def get_options(self):
    #     return self.editor.get_options()