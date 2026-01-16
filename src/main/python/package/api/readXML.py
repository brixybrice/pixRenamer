import datetime
import os
import shutil
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict

#sourceXML = '/Users/bricebarbier/Desktop/py/renameXML_source/A921_sony/A921_sony.xml'
#sourceFolder = '/Users/bricebarbier/Desktop/py/renameXML_source/A921_sony'



def get_date() -> str:
    """get current date"""
    now = datetime.datetime.now()
    return f"{now.year:04d}-{now.month:02d}-{now.day:02d}_{now.hour:02d}-{now.minute:02d}-{now.second:02d}"


def _safe_target_path(folder: str, filename: str) -> str:
    """Return a non-colliding path by appending _1, _2, ... if needed."""
    base = Path(folder) / filename
    if not base.exists():
        return str(base)

    stem = base.stem
    suffix = base.suffix
    for n in range(1, 1000):
        candidate = base.with_name(f"{stem}_{n}{suffix}")
        if not candidate.exists():
            return str(candidate)
    raise RuntimeError(f"Unable to find a free filename for: {base}")

def rename_files_from_XML(
    sourceXML,
    sourceFolder,
    archiveValue,
    sourceFilenameValue,
    circledTakesValue,
    alexa35,
    digits_shot,
    digits_take,
    episode_val,
):
    print(f'circled takes value : {circledTakesValue}')
    print(f'archive value : {archiveValue}')
    print(f'source filename value : {sourceFilenameValue}')
    print(f'apply alexa 35 trick : {alexa35}')
    print(f'apply 2 digits value for shots : {digits_shot}')
    print(f'apply 2 digits value for takes : {digits_take}')
    print(f'apply episode value : {episode_val}')

    keep_original_files = archiveValue

    reverse_data = {
        "version": 1,
        "archive_enabled": archiveValue,
        "source_folder": sourceFolder,
        "files": []
    }

    count = 0
    tree = ET.parse(sourceXML)
    root = tree.getroot()

    # ------------------------------------------------------------------
    # PRE-SIMULATION: detect filename collisions BEFORE touching disk
    # ------------------------------------------------------------------

    generated_map = defaultdict(set)  # logical_name -> {source clip names}

    for clip in root.findall('Folder/Content/VideoClip'):
        clipname = clip[1][0].text

        # Alexa35 name normalization
        if alexa35 is True:
            clipname = clipname.replace('h', 'a')

        episode = clip[2][0].text
        scene = clip[2][1].text
        shot = clip[2][2].text
        take = clip[2][3].text

        if shot and digits_shot:
            shot = shot.zfill(digits_shot)

        if take and digits_take:
            take = take.zfill(digits_take)

        selected = clip[5][0].text
        circled = 1 if selected == 'Flagged' else 0

        # Removed filtering on circled takes here to detect all duplicates regardless of circled status

        camLetter = clip[2][4].text if clip[2][4].text else clipname[0:1]

        if episode and episode_val:
            episode = episode.replace(" ", "")
            if shot:
                newName = f'{episode}-{scene}-{shot}-{take}{camLetter}'
            else:
                newName = f'{episode}-{scene}-{take}{camLetter}'
        else:
            if shot:
                newName = f'{scene}-{shot}-{take}{camLetter}'
            else:
                newName = f'{scene}-{take}{camLetter}'

        if sourceFilenameValue:
            newName = f'{newName}_{clipname}'

        generated_map[newName.lower()].add(clipname)

    duplicates = {name: sources for name, sources in generated_map.items() if len(sources) > 1}

    if duplicates:
        lines = ["Duplicate output filenames detected:\n"]
        for name, sources in sorted(duplicates.items()):
            lines.append(f"{name}  <-  {', '.join(sorted(sources))}")
        raise ValueError("\n".join(lines))

    # folders
    if keep_original_files:
        # Renamed files go directly into sourceFolder, originals are copied into sourceFolder/archive
        pix_dir = sourceFolder
        archive_dir = os.path.join(sourceFolder, "archive")
        os.makedirs(archive_dir, exist_ok=True)
    else:
        # Legacy behaviour: renamed files are moved into sourceFolder/PIX, optional originals copy into sourceFolder/archive
        archive_dir = os.path.join(sourceFolder, "archive")
        if archiveValue:
            os.makedirs(archive_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # ARCHIVE SOURCE XML (if archive is enabled)
    # ------------------------------------------------------------------
    if archiveValue:
        try:
            xml_name = os.path.basename(sourceXML)
            xml_archive_path = os.path.join(archive_dir, xml_name)

            # Avoid overwriting an existing archived XML
            if not os.path.exists(xml_archive_path):
                shutil.copy2(sourceXML, xml_archive_path)
        except Exception as e:
            print(f"[WARN] Unable to archive source XML: {e}")

    log_file = open(os.path.join(sourceFolder, f"{get_date()}.log"), "w", encoding="utf-8")
    log_file.write(f'### RENAMING OPERATION FOR PIX\nStarting at {get_date()}\n\n')

    if keep_original_files:
        log_file.write('keep original files enabled (originals copied into archive folder)\n')
    else:
        if archiveValue:
            log_file.write('archiving required (copy originals into archive folder)\n')
        else:
            log_file.write('archiving is not required\n')


    # metadata reading from XML
    for clip in root.findall('Folder/Content/VideoClip'):
        clipname = clip[1][0].text
        # VERSION SPECIAL ALEXA35
        if alexa35 == True:
            clipname = clip[1][0].text.replace('h', 'a')

        episode = clip[2][0].text
        scene = clip[2][1].text
        shot = clip[2][2].text
        if shot and digits_shot:
            shot = shot.zfill(digits_shot)

        take = clip[2][3].text
        if take and digits_take:
            take = take.zfill(digits_take)

        selected = clip[5][0].text

        #print(selected)


        if selected == 'Flagged':
            circled = 1
        else:
            circled = 0

        #print(circled)

        if clip[2][4].text != '':
            camLetter = clip[2][4].text
        else:
            camLetter = clipname[0:1]

        if episode != '' and episode != None and episode_val == True:
            episode = episode.replace(" ", "")
            if shot != '' and shot != None:
                newName = f'{episode}-{scene}-{shot}-{take}{camLetter}'
            else:
                newName = f'{episode}-{scene}-{take}{camLetter}'
        else:
            if shot != '' and shot != None:
                newName = f'{scene}-{shot}-{take}{camLetter}'
            else:
                newName = f'{scene}-{take}{camLetter}'

        if sourceFilenameValue == True:
            newName = f'{newName}_{clipname}'

        for racine, dirs, files in os.walk(sourceFolder):
            # never traverse app-generated folders
            if "archive" in dirs:
                dirs.remove("archive")
            if "PIX" in dirs:
                dirs.remove("PIX")

            for i in files:
                # Match common video extensions for the clip name
                base, ext = os.path.splitext(i)
                if base != clipname:
                    continue
                if ext.lower() not in {".mov", ".mp4"}:
                    continue

                src_path = os.path.join(racine, i)
                original_path = src_path
                archived_path = None
                renamed_path = None

                # Option: only keep circled takes
                if circledTakesValue and circled != 1:
                    if archiveValue:
                        archive_copy_path = _safe_target_path(archive_dir, i)
                        shutil.move(src_path, archive_copy_path)
                    else:
                        os.remove(src_path)
                    continue

                dst_name = f"{newName}{ext.lower()}"

                if archiveValue:
                    # 1) Move original into archive (sourceFolder will contain NO original files)
                    archive_copy_path = _safe_target_path(archive_dir, i)
                    shutil.move(src_path, archive_copy_path)
                    archived_path = archive_copy_path

                    # 2) Copy renamed file into sourceFolder root
                    dst_in_root = _safe_target_path(sourceFolder, dst_name)
                    shutil.copy2(archive_copy_path, dst_in_root)
                    renamed_path = dst_in_root
                else:
                    # Destructive mode: rename original in place
                    dst_in_place = _safe_target_path(racine, dst_name)
                    os.rename(src_path, dst_in_place)
                    renamed_path = dst_in_place

                reverse_data["files"].append({
                    "original_path": original_path,
                    "renamed_path": renamed_path,
                    "archived_path": archived_path
                })

                print(f"[#{count}] {i} --> {dst_name}")
                log_file.write(f"[#{count}] {i} --> {dst_name}\n")
                count += 1


    log_file.write(f'\n### END OF OPERATION at {get_date()}')
    log_file.close()
    return count, reverse_data

#rename_files_from_XML(sourceXML, sourceFolder)