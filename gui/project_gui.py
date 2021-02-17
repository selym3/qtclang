####################
# QTCLANG GUI CODE #
####################

# this code is less bad than the executable code

from PyQt5 import QtWidgets

class ProgramApp(QtWidgets.QWidget):

    def __init__(self, program_manager, width, height):
        super(ProgramApp, self).__init__()
        self.setFixedSize(width, height)
        self.manager = program_manager
        self.setWindowTitle("qtclang")

        # Create root form layout
        self.root = QtWidgets.QFormLayout()

        # Assign important components
        self.args_box = QtWidgets.QLineEdit()
        self.flags_box = QtWidgets.QLineEdit()
        self.src_flags_box = QtWidgets.QLineEdit()

        # Add all sub components
        self.root.addRow(self.get_config_area())

        # get the rows before the the source is added
        self.rows_before = self.root.rowCount()
        self.root.addRow(self.get_source_area())

        # Add root layout to window
        self.setLayout(self.root)

    ###
    # CONFIGURATION AREA CODE
    ##

    def get_config_area(self):
        
        options_box = QtWidgets.QGroupBox('Options')
        layout = QtWidgets.QFormLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(options_box)
        scroll_area.setWidgetResizable(True)

        ### ADD BUTTONS HERE ###

        layout.addRow(
            QtWidgets.QLabel('Program arguments: '),
            self.args_box
        )

        layout.addRow(
            QtWidgets.QLabel('Program compilation flags: '),
            self.flags_box
        )

        layout.addRow(
            QtWidgets.QLabel('Source file compilation flags: '),
            self.src_flags_box
        )

        run_button = QtWidgets.QPushButton('Run Program')
        run_button.clicked.connect(
            lambda: CmdExecutable("./" + self.manager.get_program_output(self.get_args())).execute()
        )
        layout.addRow(run_button)

        compile_button = QtWidgets.QPushButton('Compile Program')
        compile_button.clicked.connect(
            lambda: self.manager.get_program_exec_with_flags(self.get_flags()).execute()
        )
        layout.addRow(compile_button)

        compile_all = QtWidgets.QPushButton('Compile All Sources')
        compile_all.clicked.connect(
            lambda: Executables(self.manager.get_source_execs(self.get_src_flags())).execute()
        )
        layout.addRow(compile_all)

        refresh = QtWidgets.QPushButton('Refresh sources')
        refresh.clicked.connect(
            lambda: self.refresh_sources()
        )
        layout.addRow(refresh)

        ########################

        options_box.setLayout(layout)

        return scroll_area

    def get_args(self):
        return self.args_box.text()

    def get_src_flags(self):
        return self.src_flags_box.text()

    def get_flags(self):
        return self.flags_box.text()

    ###
    # SOURCE AREA CODE
    ###

    def get_source_area(self):
        
        source_box = QtWidgets.QGroupBox('Sources')
        layout = QtWidgets.QFormLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(source_box)
        scroll_area.setWidgetResizable(True)

        for source in self.manager.get_source_paths():
            self.add_source(layout, source)

        source_box.setLayout(layout)

        return scroll_area

    def add_source(self, layout, source):
        out = self.manager.get_source_output(source)

        title = QtWidgets.QLabel(source)
        button = QtWidgets.QPushButton('Compile Source (' + out + ')')

        button.clicked.connect(lambda: self.manager.get_source_exec(source, self.get_src_flags()).execute())

        layout.addRow(title, button)

    def refresh_sources(self):
        if self.root.rowCount() == self.rows_before + 1:
            self.root.removeRow(self.rows_before)

        self.root.addRow(self.get_source_area())
