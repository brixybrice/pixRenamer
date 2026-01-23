source venv3/bin/activate
cd ~/PycharmProjects/pyside2/pixRenamer
fbs clean
fbs freeze
#!/bin/bash

rm -rf build dist

set -e

# Activer l'environnement virtuel
source venv3/bin/activate

# Se placer à la racine du projet
cd ~/PycharmProjects/pyside2/pixRenamer

# Nettoyage des anciens builds PyInstaller
rm -rf build dist __pycache__

# Build de l'application avec PyInstaller (PySide6, sans fbs)
pyinstaller pixRenamer.spec --clean --noconfirm

# Vérification de l'existence de l'app
APP_PATH="dist/Pix Renamer.app"

if [ ! -d "$APP_PATH" ]; then
    echo "Erreur : l'application n'a pas été générée."
    exit 1
fi

# Ouverture du dossier contenant l'application
open dist

echo "Build terminé avec succès."
echo "Application disponible dans : $APP_PATH"

APP_NAME="Pix Renamer"
DMG_NAME="Pix_Renamer.dmg"
TMP_DMG="dist/tmp.dmg"

rm -f "dist/$DMG_NAME"
rm -f "$TMP_DMG"

hdiutil create -volname "$APP_NAME" -srcfolder "dist/$APP_NAME.app" -ov -format UDZO "$TMP_DMG"

hdiutil convert "$TMP_DMG" -format UDZO -o "dist/$DMG_NAME"

rm -f "$TMP_DMG"

create-dmg \
  --volname "${APP_NAME}" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 120 \
  --icon "${APP_NAME}.app" 150 200 \
  --app-drop-link 450 200 \
  "${DMG_NAME}" \
  "dist"
