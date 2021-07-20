from PyQt5.QtWidgets import * # QScrollArea, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *

class CompilerOptions:

    def from_file(filepath):
        # this doesnt give any good messages for incomplete files 
        # or files too long

        data = []
        with open(filepath) as f:
            line = None
            while len(data) < 2 and line != '':
                data += [ f.readline().strip() ]
        
        return CompilerOptions(*data)
                
    def __init__(self, compiler, flags):
        self.compiler = compiler
        self.flags = flags

    def __str__(self):
        return f"{self.compiler}\n{self.flags}"

DEFAULT_OPTS = CompilerOptions(
    "clang++",
    "-O3 -std=c++17 -pthread"
)

class CompilerTab(QScrollArea):

    def __init__(self, parent):
        super().__init__(parent)
        # self.parent = parent

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
        fname = QFileDialog().getOpenFileName(
            self, 
            'Select Configuration File', # <-- file dialog name 
            '', # <-- directory to start file exploraton from
            "qtclang configuration (*.qtclang)" # <-- filter
        )
        
        if (fname is not None) and fname[0] != '':
            print("Opening config file", fname)
            opts = CompilerOptions.from_file(fname[0])
            print(opts)

            self.load_options(opts)
        else:
            print("Didn't find file")

    def save_config(self):
        fname = QFileDialog().getSaveFileName(
            self,
            'Choose a save file name',
            '',
            'qtclang configuration (*.qtclang)' 
        )

        print("Saving file", fname)
        if (fname is not None) and fname[0] != '':
            opts = self.get_options()
            real_name = fname[0]
            if not real_name.endswith('.qtclang'):
                real_name += '.qtclang'

            with open(real_name, 'w') as f:
                f.write(str(opts))
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