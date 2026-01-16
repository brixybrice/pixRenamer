import os
import sys


def resource_path(relative_path: str) -> str:
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

    # Development mode
    project_root = os.path.abspath(
        os.path.join(executable_dir, "..", "..", "..")
    )
    return os.path.join(project_root, "src", relative_path)