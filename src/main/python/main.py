import os
import sys

from PySide6.QtWidgets import QApplication

from package.main_window import MainWindow

def resource_path(relative_path):
    """
    Resolve resource paths for:
    - development
    - PyInstaller onefile
    - PyInstaller onedir (.app on macOS)
    """
    # PyInstaller onefile
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    executable_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # PyInstaller onedir (.app on macOS)
    if executable_dir.endswith(os.path.join("Contents", "MacOS")):
        contents_dir = os.path.dirname(executable_dir)
        resources_dir = os.path.join(contents_dir, "Resources")
        return os.path.join(resources_dir, relative_path)

    # Development mode (src/main/python)
    project_root = os.path.abspath(
        os.path.join(executable_dir, "..", "..", "..")
    )
    return os.path.join(project_root, "src", relative_path)

def load_stylesheet(app):
    css_path = resource_path("resources/base/style.css")

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    # Resolve SVG paths for Qt CSS (relative paths do not work in PyInstaller)
    arrow_up = resource_path("resources/icons/arrow_up.svg").replace("\\", "/")
    arrow_down = resource_path("resources/icons/arrow_down.svg").replace("\\", "/")

    css = css.replace(
        "image: url(../../resources/icons/arrow_up.svg);",
        f"image: url({arrow_up});"
    )

    css = css.replace(
        "image: url(../../resources/icons/arrow_down.svg);",
        f"image: url({arrow_down});"
    )

    app.setStyleSheet(css)

def main() -> int:
    # macOS: improves rendering for some Qt builds
    os.environ.setdefault("QT_MAC_WANTS_LAYER", "1")

    app = QApplication(sys.argv)
    load_stylesheet(app)
    window = MainWindow()
    window.resize(350, 150)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
