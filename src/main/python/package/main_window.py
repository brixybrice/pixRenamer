from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIcon
from package.api.readXML import rename_files_from_XML
# from package.api.readJSON import read_data_from_json, write_data_json  # legacy (disabled)
from package.workers.rename_worker import RenameWorker
from package.api.reverseJSON import reverse_from_json
from package.utils.resources import resource_path
from package.utils.settings import load_settings, save_settings
import os
import subprocess


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pix Renamer")

        # Load persisted settings first (must not depend on UI being created)
        self.sourceFolder = ""
        self.sourceXML = ""
        self.settings = load_settings()

        # Ensure settings file exists on first launch
        if not self.settings:
            self.settings = {
                "shot_digits": 1,
                "take_digits": 1,
                "archive": False,
                "filename": False,
                "circled": False,
                "episode": False,
                "last_folder": "",
                "last_xml": "",
            }
            save_settings(self.settings)

        # Build UI
        self.create_menu()
        self.setup_ui()

        # Apply settings safely (widgets exist now)
        self.spin_shot_digits.setValue(int(self.settings.get("shot_digits", 2)))
        self.spin_take_digits.setValue(int(self.settings.get("take_digits", 2)))
        self.btn_archive.setChecked(bool(self.settings.get("archive", False)))
        self.btn_filename.setChecked(bool(self.settings.get("filename", False)))
        self.btn_circledTakes.setChecked(bool(self.settings.get("circled", False)))
        self.btn_episode.setChecked(bool(self.settings.get("episode", False)))

        self.sourceFolder = self.settings.get("last_folder", "") or ""
        self.sourceXML = self.settings.get("last_xml", "") or ""

        # Enable rename only when both paths are set
        self.btn_rename.setEnabled(bool(self.sourceFolder and self.sourceXML))


    def create_menu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        file_menu = self.menubar.addMenu("File")

        self.action_reverse = QtGui.QAction("Reverse from JSON", self)
        file_menu.addAction(self.action_reverse)

        self.action_reverse.triggered.connect(self.reverse_from_json)


    def reverse_from_json(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setNameFilters(["JSON (*.json)"])
        if file_dialog.exec() != QtWidgets.QDialog.Accepted:
            return

        json_path = file_dialog.selectedUrls()[0].toLocalFile()

        try:
            count = reverse_from_json(json_path)
            QtWidgets.QMessageBox.information(
                self,
                "Reverse completed",
                f"{count} files have been restored"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Reverse error", str(e))

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
        # self.btn_alexa35 = QtWidgets.QCheckBox("replace \"h\" with \"a\" (alexa35 with Daylight)")
        self.shot_digits_label = QtWidgets.QLabel("Shot digits")
        self.spin_shot_digits = QtWidgets.QSpinBox()
        self.spin_shot_digits.setRange(1, 9)
        self.spin_shot_digits.setValue(2)
        self.spin_shot_digits.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spin_shot_digits.setFixedHeight(30)
        font = self.spin_shot_digits.font()
        font.setPointSize(font.pointSize() + 1)
        self.spin_shot_digits.setFont(font)
        self.take_digits_label = QtWidgets.QLabel("Take digits")
        self.spin_take_digits = QtWidgets.QSpinBox()
        self.spin_take_digits.setRange(1, 9)
        self.spin_take_digits.setValue(2)
        self.spin_take_digits.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spin_take_digits.setFixedHeight(30)

        font = self.spin_take_digits.font()
        font.setPointSize(font.pointSize() + 1)
        self.spin_take_digits.setFont(font)
        self.btn_episode = QtWidgets.QCheckBox("start the naming with episode")

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 0)  # indéterminée
        self.progress.setVisible(False)


    def modify_widgets(self):
        self.btn_rename.setEnabled(False)
        self.btn_rename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sourceFolder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sourceXML.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_archive.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_filename.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.spin_shot_digits.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.spin_take_digits.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setMenuBar(self.menubar)
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
        # self.main_layout.addWidget(self.btn_alexa35)
        digits_container = QtWidgets.QWidget()
        digits_layout = QtWidgets.QHBoxLayout(digits_container)
        digits_layout.setContentsMargins(0, 8, 0, 8)
        digits_layout.setSpacing(12)

        digits_layout.addWidget(self.shot_digits_label)
        digits_layout.addWidget(self.spin_shot_digits)
        digits_layout.addSpacing(24)
        digits_layout.addWidget(self.take_digits_label)
        digits_layout.addWidget(self.spin_take_digits)
        self.main_layout.addWidget(self.btn_episode)
        digits_layout.addStretch()

        self.spin_shot_digits.setFixedWidth(70)
        self.spin_take_digits.setFixedWidth(70)

        self.main_layout.addWidget(digits_container)

        self.main_layout.addWidget(self.btn_rename)

        self.main_layout.addWidget(self.progress)


    def setup_connections(self):
        self.btn_sourceFolder.clicked.connect(self.choose_source_folder)
        self.btn_sourceXML.clicked.connect(self.choose_xml_file)
        self.btn_rename.clicked.connect(self.rename_files)

    def rename_files(self):
        self.btn_rename.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # spinner

        save_settings({
            "shot_digits": self.spin_shot_digits.value(),
            "take_digits": self.spin_take_digits.value(),
            "archive": self.btn_archive.isChecked(),
            "filename": self.btn_filename.isChecked(),
            "circled": self.btn_circledTakes.isChecked(),
            "episode": self.btn_episode.isChecked(),
            "last_folder": self.sourceFolder,
            "last_xml": self.sourceXML,
        })

        self.thread = QtCore.QThread()
        self.worker = RenameWorker(
            self.sourceXML,
            self.sourceFolder,
            self.btn_archive.isChecked(),
            self.btn_filename.isChecked(),
            self.btn_circledTakes.isChecked(),
            # self.btn_alexa35.isChecked(),
            False,
            self.spin_shot_digits.value(),
            self.spin_take_digits.value(),
            self.btn_episode.isChecked()
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_rename_finished)
        self.worker.error.connect(self.on_rename_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)

        self.thread.start()

    def choose_source_folder(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if file_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.sourceFolder = file_dialog.selectedUrls()[0].toLocalFile()
            print(self.sourceFolder)
            save_settings({
                **load_settings(),
                "last_folder": self.sourceFolder
            })
            if self.sourceXML != '':
                self.btn_rename.setEnabled(True)

    def choose_xml_file(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setDefaultSuffix('xml')
        file_dialog.setNameFilters(['XML (*.xml)'])
        if file_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.sourceXML = file_dialog.selectedUrls()[0].toLocalFile()
            print(self.sourceXML)
            save_settings({
                **load_settings(),
                "last_xml": self.sourceXML
            })
            if self.sourceFolder != '':
                self.btn_rename.setEnabled(True)

    def on_rename_finished(self, count):
        self.btn_rename.setEnabled(True)
        self.progress.setVisible(False)

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Rename completed")

        if count == 0:
            msg.setText("There is no file to be renamed")
            msg.addButton(QtWidgets.QMessageBox.Ok)
        else:
            msg.setText(f"{count} files have been successfully renamed")
            open_btn = msg.addButton("Open Folder", QtWidgets.QMessageBox.ActionRole)
            msg.addButton(QtWidgets.QMessageBox.Ok)

        msg.exec()

        if count > 0 and msg.clickedButton() == open_btn:
            latest = load_settings()
            last_folder = self.sourceFolder or latest.get("last_folder", "")

            if last_folder and os.path.exists(last_folder):
                subprocess.run(["open", last_folder])

    def on_rename_error(self, message):
        # Stop any progress indication (duplicates = no operation performed)
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)
        self.btn_rename.setEnabled(True)

        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Rename aborted")

        msg.setText(
            "Some files would generate identical output filenames.\n"
            "No file has been modified."
        )

        # Show ALL duplicates in the expandable details section
        msg.setDetailedText(message)

        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec()

    def closeEvent(self, event):
        save_settings({
            "shot_digits": self.spin_shot_digits.value(),
            "take_digits": self.spin_take_digits.value(),
            "archive": self.btn_archive.isChecked(),
            "filename": self.btn_filename.isChecked(),
            "circled": self.btn_circledTakes.isChecked(),
            "episode": self.btn_episode.isChecked(),
            "last_folder": self.sourceFolder,
            "last_xml": self.sourceXML,
        })
        event.accept()
