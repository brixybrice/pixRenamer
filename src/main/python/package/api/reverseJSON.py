import json
import os
import shutil
from datetime import datetime


def write_reverse_json(source_folder: str, reverse_data: dict) -> str:
    """
    Write a portable reverse JSON using relative paths.
    """
    base = os.path.abspath(source_folder)
    reverse_data["source_folder"] = "."

    for entry in reverse_data["files"]:
        entry["original_path"] = os.path.relpath(entry["original_path"], base)
        entry["renamed_path"] = os.path.relpath(entry["renamed_path"], base)
        if entry["archived_path"]:
            entry["archived_path"] = os.path.relpath(entry["archived_path"], base)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(base, f"pixRenamer_reverse_{timestamp}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reverse_data, f, indent=4)

    return json_path


def reverse_from_json(json_path: str) -> int:
    """
    Restore all files to their original location using a PixRenamer reverse JSON.
    All files are restored into the source folder, including archived ones.
    Works even if the folder has been moved.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "files" not in data:
        raise ValueError("Invalid reverse JSON")

    # Base folder = folder containing the JSON (portable root)
    base = os.path.dirname(os.path.abspath(json_path))

    restored = 0

    for entry in data["files"]:
        original_rel = entry.get("original_path")
        renamed_rel = entry.get("renamed_path")
        archived_rel = entry.get("archived_path")

        if not original_rel:
            continue

        final_path = os.path.join(base, original_rel)

        # Possible current locations of the file
        candidates = []

        if renamed_rel:
            candidates.append(os.path.join(base, renamed_rel))

        if archived_rel:
            candidates.append(os.path.join(base, archived_rel))

        source_file = next((p for p in candidates if p and os.path.exists(p)), None)
        if not source_file:
            continue

        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        shutil.move(source_file, final_path)
        restored += 1

    return restored