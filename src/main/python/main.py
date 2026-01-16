import os
import sys

from PySide6.QtWidgets import QApplication

from package.main_window import MainWindow


def main() -> int:
    # macOS: improves rendering for some Qt builds
    os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(350, 150)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
