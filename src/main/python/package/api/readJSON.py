import json
import os
import sys
from pathlib import Path


def _app_support_dir(app_name: str) -> Path:
    """Return a per-user config directory for the current OS."""
    home = Path.home()

    # macOS
    if sys.platform == "darwin":
        base = home / "Library" / "Application Support"
        return base / app_name

    # Windows
    if os.name == "nt":
        base = os.getenv("APPDATA")
        if base:
            return Path(base) / app_name
        # Fallback (rare): use home
        return home / "AppData" / "Roaming" / app_name

    # Linux and others
    xdg = os.getenv("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / app_name
    return home / ".config" / app_name


def _options_path() -> Path:
    return _app_support_dir("pixRenamer") / "options.json"


_DEFAULT_OPTIONS = {
    "circledTakesValue": True,
    "archiveValue": False,
    "sourceFilenameValue": False,
    "alexa35": False,
    "digits_shot": False,
    "digits_take": False,
    "episode_val": False,
}


def read_data_from_json() -> dict:
    path = _options_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Backward/forward compatibility: ensure all keys exist
        merged = dict(_DEFAULT_OPTIONS)
        merged.update({k: data.get(k, v) for k, v in _DEFAULT_OPTIONS.items()})
        return merged

    # Create defaults on first run
    with path.open("w", encoding="utf-8") as f:
        json.dump(_DEFAULT_OPTIONS, f, indent=4)
    return dict(_DEFAULT_OPTIONS)


def write_data_json(
    archive: bool,
    filename: bool,
    circledTakes: bool,
    alexa35: bool,
    digit_shot: bool,
    digit_take: bool,
    episode_val: bool,
) -> None:
    path = _options_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    current = read_data_from_json()
    current["circledTakesValue"] = bool(circledTakes)
    current["archiveValue"] = bool(archive)
    current["sourceFilenameValue"] = bool(filename)
    current["alexa35"] = bool(alexa35)
    current["digits_shot"] = bool(digit_shot)
    current["digits_take"] = bool(digit_take)
    current["episode_val"] = bool(episode_val)

    with path.open("w", encoding="utf-8") as f:
        json.dump(current, f, indent=4)
