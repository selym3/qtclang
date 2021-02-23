####################
# QTCLANG GUI CODE #
####################

# this code is less bad than the executable code

import os

from app.executable import Executable
from app.file_manager import FileManager
from PyQt5 import QtWidgets


class ProgramApp(QtWidgets.QWidget):

    def __init__(self, program_manager, width, height):
        super(ProgramApp, self).__init__()

        # TODO: make a command line option or selectable
        self.fm = FileManager('./.qtclang')

        self.setFixedSize(width, height)
        self.manager = program_manager
        self.setWindowTitle("qtclang")

        # Create root form layout
        self.root = QtWidgets.QFormLayout()

        # Assign important components
        self.args_box = QtWidgets.QLineEdit()
        self.flags_box = QtWidgets.QLineEdit()
        self.src_flags_box = QtWidgets.QLineEdit()
        
        self.output_button = QtWidgets.QCheckBox("Toggle Command Output")
        self.output_button.setChecked(True)

        # Add all sub components
        self.root.addRow(self.get_config_area())

        # get the rows before the the source is added
        self.rows_before = self.root.rowCount()
        self.root.addRow(self.get_source_area())

        # Add root layout to window
        self.setLayout(self.root)

        # Do final initialization here
        self.load_options()

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
            lambda: (self.manager.run_exc(self.get_args())).execute(self.should_output())
        )
        layout.addRow(run_button)

        compile_button = QtWidgets.QPushButton('Compile Program')
        compile_button.clicked.connect(
            lambda: (self.manager.program_exc(self.get_flags())).execute(self.should_output())
        )
        layout.addRow(compile_button)

        compile_all = QtWidgets.QPushButton('Compile All Sources')
        compile_all.clicked.connect(
            lambda: (self.all_sources()).execute(self.should_output())
        )
        layout.addRow(compile_all)

        refresh = QtWidgets.QPushButton('Refresh sources')
        refresh.clicked.connect(
            lambda: self.refresh_sources()
        )
        layout.addRow(refresh)

        layout.addRow(
            # QtWidgets.QLabel('Toggle debug mode: '),
            self.output_button
        )

        # add file io buttons

        save_button = QtWidgets.QPushButton('Save Config')
        save_button.clicked.connect(
            lambda: self.save_options()
        )

        load_button = QtWidgets.QPushButton('Load Config')
        load_button.clicked.connect(
            lambda: self.load_options()
        )

        layout.addRow(
            save_button
        )
        layout.addRow(
            load_button
        )

        # test
        # save_file = QtWidgets.QPushButton('Save File')
        # save_file.clicked.connect(
        #     lambda: self.testFile()
        # )
        # layout.addRow(save_file)

        ########################

        options_box.setLayout(layout)

        return scroll_area
    
    # def testFile(self):
    #     options = QtWidgets.QFileDialog.Options()
    #     options |= QtWidgets.QFileDialog.DontUseNativeDialog
    #     fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"test -- open a file","","qtclang Files (*.qtclang)", options=options)
    #     if fileName:
    #         print(fileName)

    def all_sources(self):
        sources = self.manager.sources()
        sources = (self.manager.source_cmd(source, self.get_src_flags()) for source in sources)

        return Executable.many(sources)

    def should_output(self):
        return self.output_button.isChecked()

    def get_args(self):
        return self.args_box.text()

    def get_src_flags(self):
        return self.src_flags_box.text()

    def get_flags(self):
        return self.flags_box.text()

    def clean_option(self, opt):
        return opt.replace('\n', '')

    def get_options(self):
        out = self.get_args(), self.get_flags(), self.get_src_flags(), self.should_output()

        return out

    def save_options(self):
        self.fm.clear()
        options = self.get_options()
        self.fm.write(options, lines=True)
    
    def load_options(self):
        new_options = self.fm.text()
        old_options = self.get_options()

        if new_options == None or len(new_options) < len(old_options):
            print("Options file not found... Try saving first!")
            return

        new_options = [self.clean_option(option) for option in new_options]
        
        self.args_box.setText(new_options[0])
        self.flags_box.setText(new_options[1])
        self.src_flags_box.setText(new_options[2])
        self.output_button.setChecked(new_options[3] == str(True))
        

    ###
    # SOURCE AREA CODE
    ###

    def get_source_area(self):
        
        source_box = QtWidgets.QGroupBox('Sources')
        layout = QtWidgets.QFormLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(source_box)
        scroll_area.setWidgetResizable(True)

        for source in self.manager.sources():
            self.add_source(layout, source)

        source_box.setLayout(layout)

        return scroll_area

    def add_source(self, layout, source):
        out = self.manager.source_out(source)

        title = QtWidgets.QLabel(source)
        button = QtWidgets.QPushButton('Compile (' + out + ')')

        button.clicked.connect(lambda: self.manager.source_exc(source, self.get_src_flags()).execute(self.should_output()) )

        layout.addRow(title, button)

    def refresh_sources(self):
        if self.root.rowCount() == self.rows_before + 1:
            self.root.removeRow(self.rows_before)

        self.root.addRow(self.get_source_area())
