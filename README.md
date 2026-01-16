# PixRenamer

PixRenamer is a Python desktop application with a graphical interface designed to **automatically rename video files based on XML shooting metadata**, while ensuring a **safe, deterministic, and post-production–ready workflow**.

It is built for film and television pipelines where filename consistency, traceability, and media safety are critical.

---

## Features

- Automatic renaming of video files (`.mov`, `.mp4`) using XML metadata
- Standardized filename generation including:
  - episode
  - scene
  - shot
  - take
  - camera letter
  - optional original clip name
- Support for **flagged / circled takes only**
- Automatic filename collision handling (`_1`, `_2`, …)
- Timestamped log file generated for every operation
- Safe and explicit archive workflow
- Apple Silicon compatible macOS application

---

## Operating Modes

### Archive Mode Enabled (safe / non-destructive)

When **Archive Mode** is enabled:

1. All original source files are **moved** into an `archive/` folder  
2. Renamed files are **copied** into the root of the source folder  
3. The source folder ends up containing **only renamed files**  
4. All originals are stored in `archive/`  
5. A log file is written at the root of the source folder  

Final structure:

```
sourceFolder/
├─ renamed_files.mov
├─ renamed_files.mp4
├─ archive/
│  └─ original_files.mov
└─ YYYY-MM-DD_HH-MM-SS.log
```

This mode guarantees:
- no loss of original media
- clean separation between sources and deliverables
- fully reversible workflows

---

### Archive Mode Disabled (destructive)

When **Archive Mode** is disabled:

- Files are renamed **in place**
- No archive is created
- Intended for already validated or disposable media sets

---

## Requirements

### Runtime (end users)

- macOS (Apple Silicon)
- No Python installation required when using the packaged `.app`

### Development

- Python 3.10 or later
- PySide6
- PyInstaller (for building the macOS app)

---

## Installation

### Option 1 — Use the macOS Application

1. Download the latest `PixRenamer.app`
2. Move it to `/Applications` or any preferred location
3. Launch the app

If macOS blocks the app on first launch:
- Right-click the app
- Choose **Open**
- Confirm the security prompt

---

### Option 2 — Run from Source (development)

Clone the repository:

```bash
git clone https://github.com/yourname/pixrenamer.git
cd pixrenamer
```

Create and activate a virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install PySide6
```

Run the application:

```bash
python src/main/python/main.py
```

---

## Usage

1. Launch PixRenamer
2. Select:
   - the **source folder** containing the media files
   - the **XML file** containing shooting metadata
3. Configure options:
   - enable or disable **Archive Mode**
   - process **flagged takes only**
   - enable zero-padding for shots and takes
   - include original clip name if required
   - Alexa 35 filename handling if applicable
4. Run the operation

After completion:
- renamed files are available in the source folder
- original files are in `archive/` if archive mode was enabled
- a timestamped `.log` file is available at the root

---

## Logging

Each operation generates a log file at the root of the source folder:

```
YYYY-MM-DD_HH-MM-SS.log
```

The log includes:
- configuration used
- every file processed
- original filename → new filename mapping
- operation start and end timestamps

---

## Safety Guarantees

- No file overwriting
- Automatic collision-safe filenames
- No accidental deletions when archive mode is enabled
- Strict and predictable file operation order
- Deterministic results across multiple runs

---

## Typical Use Cases

- Rushes conformation after shooting
- Filename normalization for editorial, VFX, and grading
- Securing original media before renaming
- Preparing clean PIX delivery folders
- Automating DIT and assistant editor workflows

---

## Technical Stack

- Python 3.10+
- PySide6 (GUI)
- PyInstaller (macOS packaging)
- Apple Silicon (arm64)

---

## License

MIT License
