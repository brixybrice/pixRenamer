from PySide6.QtCore import QObject, Signal, Slot
from package.api.readXML import rename_files_from_XML
from package.api.reverseJSON import write_reverse_json


class RenameWorker(QObject):
    progress = Signal(int)
    finished = Signal(int)
    error = Signal(str)

    def __init__(
        self,
        sourceXML,
        sourceFolder,
        archive,
        sourceFilename,
        circled,
        alexa35,
        digits_shot,
        digits_take,
        episode
    ):
        super().__init__()
        self.args = (
            sourceXML,
            sourceFolder,
            archive,
            sourceFilename,
            circled,
            alexa35,
            digits_shot,
            digits_take,
            episode
        )

    @Slot()
    def run(self):
        try:
            # NOTE : pour l’instant progress = indéterminé
            count, reverse_data = rename_files_from_XML(*self.args)

            write_reverse_json(self.args[1], reverse_data)

            self.finished.emit(count)

        except Exception as e:
            self.error.emit(str(e))