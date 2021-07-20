from PyQt5.QtWidgets import * # QScrollArea, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *

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

class CompilerTab(QScrollArea):

    def __init__(self, parent):
        super().__init__(parent)
        # self.parent = parent

        # Initialize non-gui members

        self.file_converter = SimpleFileProtocol()

        # Create root widget

        self.root = QGroupBox()
        self.form = self.create_root()
        self.root.setLayout(self.form)

        # Initialize form

        self.load_options(DEFAULT_OPTS)

        # Make root widget the focus of the scroll area

        self.setWidget(self.root)
        self.setWidgetResizable(True)

    def create_root(self):
        form = QFormLayout()

        # Compiler Options

        compiler_menu = QGroupBox("Options")
        compiler_menu.setLayout(self.create_compiler_menu())
        form.addRow(compiler_menu)

        # Compiler Saves

        save_menu = QGroupBox("Save / Load")
        save_menu.setLayout(self.create_save_menu())
        form.addRow(save_menu)

        # Compiler Presets

        presets = QGroupBox("Presets")
        presets.setLayout(self.create_presets())
        form.addRow(presets)
    
        return form

    def create_compiler_menu(self):

        form = QFormLayout()

        self.compiler_input = QLineEdit()
        form.addRow(
            QLabel("Compiler: "),
            self.compiler_input
        )

        self.flags_input = QLineEdit()
        form.addRow(
            QLabel("Flags: "),
            self.flags_input
        )

        return form

    def create_save_menu(self):
        
        form = QFormLayout()

        load_file = QPushButton("Load Configuration")
        load_file.clicked.connect(self.load_save_file)
        form.addRow(load_file)

        save = QPushButton("Save Configuration")
        save.clicked.connect(self.save_config)
        form.addRow(save)

        return form

    def load_save_file(self):
        fname, _ = QFileDialog().getOpenFileName(
            self, 
            'Select Configuration File', # <-- file dialog name 
            '', # <-- directory to start file exploraton from
            "qtclang configuration (*.qtclang)" # <-- filter
        )
        
        if fname != '':
            options = self.file_converter.file_to_options(fname)
            self.load_options(options)
        else:
            print("Didn't find file to load")

    def save_config(self):
        fname, _ = QFileDialog().getSaveFileName(
            self,
            'Choose a save file name',
            '',
            'qtclang configuration (*.qtclang)' 
        )

        print("Saving file", fname)
        if fname != '':
            if not fname.endswith('.qtclang'):
                fname += '.qtclang'

            self.file_converter.write_options(fname, self.get_options())
        else:
            print("Didn't find file")

    def create_presets(self):

        form = QFormLayout()

        for i in range(3):    
            default = QPushButton("Default")
            default.clicked.connect(lambda: self.load_options(DEFAULT_OPTS))
            form.addRow(default)

        return form

    def load_options(self, options):

        self.compiler_input.setText(options.compiler)
        self.flags_input.setText(options.flags)

    def get_options(self):

        out = CompilerOptions(
            self.compiler_input.text(),
            self.flags_input.text()
        )

        return out