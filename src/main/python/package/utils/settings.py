import json
import os
from pathlib import Path


APP_NAME = "pixRenamer"
COMPANY = "Be4Post"


def get_settings_path():
    base = Path.home() / "Library" / "Application Support" / COMPANY
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{APP_NAME}_params.json"


def load_settings():
    path = get_settings_path()
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data: dict):
    path = get_settings_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)