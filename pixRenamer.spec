# pixRenamer.spec
# Python 3.10 / PySide6 / macOS Apple Silicon (arm64)

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.osx import BUNDLE

# Collecte PySide6
hiddenimports = collect_submodules("PySide6")

a = Analysis(
    ["src/main/python/main.py"],
    pathex=["src/main/python"],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    excludes=["fbs", "fbs_runtime"],
    noarchive=False,
)

pyz = PYZ(a.pure)

# EXE : on NE CASSE PAS ce qui fonctionnait
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Pix Renamer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    target_arch="arm64",
)

# COLLECT : indispensable pour que l’app ne soit PAS vide
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Pix Renamer",
)

# BUNDLE macOS : icône + version
app = BUNDLE(
    coll,
    name="Pix Renamer.app",
    icon="assets/pixRenamer.icns",
    bundle_identifier="com.be4post.pixrenamer",
    info_plist={
        "CFBundleName": "Pix Renamer",
        "CFBundleDisplayName": "Pix Renamer",
        "CFBundleShortVersionString": "1.2.0",
        "CFBundleVersion": "1.2.0",
    },
)