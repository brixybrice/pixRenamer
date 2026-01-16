source venv3/bin/activate
cd ~/PycharmProjects/pyside2/pixRenamer
fbs clean
fbs freeze
#!/bin/bash
set -e

# Activer l'environnement virtuel
source venv3/bin/activate

# Se placer à la racine du projet
cd ~/PycharmProjects/pyside2/pixRenamer

# Nettoyage des anciens builds PyInstaller
rm -rf build dist
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