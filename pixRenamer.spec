# pixRenamer.spec
# Python 3.10 / PySide6 / macOS Apple Silicon (arm64)

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.building.osx import BUNDLE

hiddenimports = collect_submodules("PySide6")

a = Analysis(
    ["src/main/python/main.py"],
    pathex=["src/main/python"],
    binaries=[],
    datas=[("src/resources", "resources")],
    hiddenimports=hiddenimports,
    excludes=["fbs", "fbs_runtime"],
    noarchive=False,
)

pyz = PYZ(a.pure)

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

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Pix Renamer",
)

app = BUNDLE(
    coll,
    name="Pix Renamer.app",
    icon="assets/pixRenamer.icns",
    bundle_identifier="com.be4post.pixrenamer",
    info_plist={
        "CFBundleName": "Pix Renamer",
        "CFBundleDisplayName": "Pix Renamer",
        "CFBundleShortVersionString": "2.0.0",
        "CFBundleVersion": "2.0.0",
    },
)