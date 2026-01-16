from PySide6 import QtCore, QtGui, QtWidgets
from package.api.readXML import rename_files_from_XML
from package.api.readJSON import read_data_from_json, write_data_json


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pix Renamer")
        self.setup_ui()
        self.sourceFolder =""
        self.sourceXML = ""

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.btn_rename = QtWidgets.QPushButton('rename files')
        self.btn_sourceFolder = QtWidgets.QPushButton("Source Folder")
        self.btn_sourceXML = QtWidgets.QPushButton("Source XML")
        self.btn_circledTakes = QtWidgets.QCheckBox("circled takes only")
        self.btn_archive = QtWidgets.QCheckBox("keep original files (archive folder)")
        self.btn_filename = QtWidgets.QCheckBox("append source clipname in new filename")
        self.btn_alexa35 = QtWidgets.QCheckBox("replace \"h\" with \"a\" (alexa35 with Daylight)")
        self.btn_digit_shot = QtWidgets.QCheckBox("2 digits for shot values")
        self.btn_digit_take = QtWidgets.QCheckBox("2 digits for take values")
        self.btn_episode = QtWidgets.QCheckBox("start the naming with episode")


    def modify_widgets(self):
        self.btn_rename.setEnabled(False)
        self.btn_rename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sourceFolder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sourceXML.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_archive.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_filename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.btn_circledTakes.setChecked(read_data_from_json()['circledTakesValue'])
        self.btn_archive.setChecked(read_data_from_json()['archiveValue'])
        self.btn_filename.setChecked(read_data_from_json()['sourceFilenameValue'])
        self.btn_alexa35.setChecked(read_data_from_json()['alexa35'])
        self.btn_digit_shot.setChecked(read_data_from_json()['digits_shot'])
        self.btn_digit_take.setChecked(read_data_from_json()['digits_take'])
        self.btn_episode.setChecked(read_data_from_json()['episode_val'])

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.sources = QtWidgets.QWidget()
        self.sources_layout = QtWidgets.QHBoxLayout()
        self.sources.setLayout(self.sources_layout)

    def add_widgets_to_layouts(self):
        self.sources_layout.addWidget(self.btn_sourceFolder)
        self.sources_layout.addWidget(self.btn_sourceXML)
        self.main_layout.addWidget(self.sources)
        self.main_layout.addWidget(self.btn_circledTakes)
        self.main_layout.addWidget(self.btn_archive)
        self.main_layout.addWidget(self.btn_filename)
        self.main_layout.addWidget(self.btn_alexa35)
        self.main_layout.addWidget(self.btn_digit_shot)
        self.main_layout.addWidget(self.btn_digit_take)
        self.main_layout.addWidget(self.btn_episode)
        self.main_layout.addWidget(self.btn_rename)


    def setup_connections(self):
        self.btn_sourceFolder.clicked.connect(self.choose_source_folder)
        self.btn_sourceXML.clicked.connect(self.choose_xml_file)
        self.btn_rename.clicked.connect(self.rename_files)

    def rename_files(self):
        """Launch the renaming process based on the provided paths"""
        #sourceXML = '/Users/bricebarbier/Desktop/py/renameXML_source/A921_sony/A921_sony.xml'
        #sourceFolder = '/Users/bricebarbier/Desktop/py/renameXML_source/A921_sony'

        write_data_json(self.btn_archive.isChecked(),
                              self.btn_filename.isChecked(),
                              self.btn_circledTakes.isChecked(),
                              self.btn_alexa35.isChecked(),
                              self.btn_digit_shot.isChecked(),
                              self.btn_digit_take.isChecked(),
                              self.btn_episode.isChecked())

        count = rename_files_from_XML(self.sourceXML, self.sourceFolder, self.btn_archive.isChecked(), self.btn_filename.isChecked(), self.btn_circledTakes.isChecked(),  self.btn_alexa35.isChecked(), self.btn_digit_shot.isChecked(), self.btn_digit_take.isChecked(),  self.btn_episode.isChecked())
        message_box = QtWidgets.QMessageBox()
        if count == 0:
            message_box.setText(f'There is no file to be renamed')
        else:
            message_box.setText(f'{count} files have been successfully renamed')
        message_box.exec()

    def choose_source_folder(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if file_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.sourceFolder = file_dialog.selectedUrls()[0].toLocalFile()
            print(self.sourceFolder)
            if self.sourceXML != '':
                self.btn_rename.setEnabled(True)

    def choose_xml_file(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setDefaultSuffix('xml')
        file_dialog.setNameFilters(['XML (*.xml)'])
        if file_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.sourceXML = file_dialog.selectedUrls()[0].toLocalFile()
            print(self.sourceXML)
            if self.sourceFolder != '':
                self.btn_rename.setEnabled(True)



