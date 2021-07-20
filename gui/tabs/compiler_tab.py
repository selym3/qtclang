from PyQt5.QtWidgets import * # QScrollArea, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *

from .tab import Tab
from .component import Component

class CompilerOptions:

    def __init__(self, compiler, flags):
        self.compiler = compiler
        self.flags = flags

    def __str__(self):
        return f"{self.compiler}, {self.flags}"

    def __repr__(self):
        return f"CompilerOptions({self})"

DEFAULT_OPTS = CompilerOptions(
    "clang++",
    "-O3 -std=c++17 -pthread"
)

class OptionsEditor(Component):

    def __init__(self):
        super().__init__("Options")

        self.compiler_input = QLineEdit()
        self.addWidgets(QLabel("Compiler: "), self.compiler_input)

        self.flags_input = QLineEdit()
        self.addWidgets(QLabel("Flags: "), self.flags_input)

    def load_options(self, options):
        self.compiler_input.setText(options.compiler)
        self.flags_input.setText(options.flags)
    
    def get_options(self): 
        return CompilerOptions(
            self.compiler_input.text(),
            self.flags_input.text()
        )

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
            while len(data) < 2 and line != '':
                data += [ f.readline().strip() ]
        
        return CompilerOptions(*data)

    def options_to_file(self, options):
        return f"{options.compiler}\n{options.flags}"

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