from PyQt5.QtWidgets import * # QScrollArea, QGroupBox, QFormLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *

class CompilerOptions:

    def __init__(self, compiler, flags):
        self.compiler = compiler
        self.flags = flags

    def compile_source(self, source):
        pass
        # return f'{str(self) -c {source} '

    def __str__(self):
        return f'{self.compiler} {self.flags}'

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
        print(self.get_options())

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

        save_menu = QGroupBox("Save & Load")
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

        save = QPushButton("Save")
        save.clicked.connect(lambda: print("Saving..."))
        form.addRow(save)

        return form

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