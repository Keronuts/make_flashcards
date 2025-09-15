# MakeFlashcards

A tiny Windows GUI app that turns a CSV of Q/A pairs into **print-ready flashcards** (PDF): **9 cards per page**, **landscape**, with **cut lines** and **front/back** files aligned for **duplex printing (flip on long edge)**.

---

## Features

- **CSV-driven**: keep your deck in a simple `question,answer` spreadsheet.
- **Two PDFs**: one for **fronts (questions)**, one for **backs (answers)**.
- **9-up layout**: 3×3 grid, landscape, clean cut lines on every page.
- **Duplex-friendly**: fronts/backs align when printed **flip on long edge**.
- **Click-to-run** GUI: no command line required.

---

## Requirements

- **End users (installer)**: None. The installer includes everything.
- **Building from source**:
  - Python 3.9+ (Windows)
  - `reportlab`, `pyinstaller`
  - (Optional) **Inno Setup** for a Windows installer

---

## Quick Start (End Users)

1. **Install**: Run `MakeFlashcardsSetup.exe`  
   Installs to `C:\Program Files (x86)\MakeFlashcards\MakeFlashcards.exe`.
2. **Run**: Double-click **MakeFlashcards** (Start Menu or Desktop shortcut, if chosen).
3. **Pick your CSV** when prompted.
4. **Choose output PDFs** (defaults to the **same folder as the CSV**).
5. **Print**:
   - Orientation: **Landscape**
   - Duplex: **On**, **Flip on Long Edge**
   - Scale: **100%** (no “Fit to page”)

---

## CSV Format

Create a CSV with headers exactly:

```csv
question,answer
What is cloud computing?,On-demand access to shared compute, storage, and networking over the internet.
What are the three cloud service models?,IaaS, PaaS, SaaS.
What is the Shared Responsibility Model?,Provider secures the cloud; customer secures what's in the cloud.
```

- One row = one card.
- Keep commas within fields by quoting, e.g., `"IaaS, PaaS, SaaS"`.

---

## Printing Tips

- **Landscape**, duplex **flip on long edge**.
- **Cut lines** are printed on every page (vertical and horizontal grid).
- If your printer “auto-scales,” turn that off; keep it at **100%**.

---

## Building From Source (Developers)

1. **Clone / copy** the source file: `make_flashcards_gui.py`.
2. **Install dependencies**:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate
   pip install --upgrade pip
   pip install reportlab pyinstaller
   ```
3. **Run directly**:
   ```powershell
   python make_flashcards_gui.py
   ```
   You’ll get GUI dialogs (select CSV → choose output PDFs).

### Package as a Portable EXE (PyInstaller)

```powershell
pyinstaller --onefile --windowed make_flashcards_gui.py
```

- Output: `dist\make_flashcards_gui.exe`  
- Double-click to launch (no console window).

### Create a Windows Installer (Inno Setup)

1. Install **Inno Setup** (https://jrsoftware.org/).
2. Build the EXE with PyInstaller (above).
3. Use this Inno script (example) to package:

```ini
[Setup]
AppId={{A5D9B1C7-3B3D-4C4A-BF0E-0D47F7C2B2C9}
AppName=MakeFlashcards
AppVersion=1.0.0
AppPublisher=Your Name or Company
DefaultDirName={commonpf32}\MakeFlashcards
DefaultGroupName=MakeFlashcards
UninstallDisplayIcon={app}\MakeFlashcards.exe
OutputDir=.
OutputBaseFilename=MakeFlashcardsSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\MakeFlashcards.exe"; DestDir: "{app}"; DestName: "MakeFlashcards.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\MakeFlashcards"; Filename: "{app}\MakeFlashcards.exe"
Name: "{commondesktop}\MakeFlashcards"; Filename: "{app}\MakeFlashcards.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\MakeFlashcards.exe"; Description: "Launch MakeFlashcards"; Flags: nowait postinstall skipifsilent
```

Compile in Inno to produce `MakeFlashcardsSetup.exe`.

---

## Troubleshooting

- **No PDFs created**  
  - Make sure you **selected a CSV** and **chose save locations** in the dialogs.
  - If running from source: confirm `reportlab` is installed and there are no console errors.

- **“This isn’t a PDF”**  
  - Ensure your filenames end with **`.pdf`**. The GUI adds `.pdf` by default.

- **CSV error**: “must have headers question,answer”  
  - Check the first row exactly: `question,answer` (lowercase, no extra spaces).

- **Duplex misalignment**  
  - Verify **Flip on Long Edge** and **Landscape**.
  - Disable printer “fit to page”; use **100%**.

- **SmartScreen warning** (downloaded installer)  
  - Consider **code signing** your EXE/installer for smoother installs.

---

## Project Structure (typical)

```
MakeFlashcards/
├─ make_flashcards_gui.py
├─ cards.csv                # your deck (example)
├─ dist/
│  └─ MakeFlashcards.exe    # PyInstaller output
├─ MakeFlashcardsSetup.exe  # Inno Setup installer (compiled)
└─ README.md
```

---

## License

none

---

## Support / Feedback

Spotted a bug, or want a feature (e.g., 6-up vs 9-up toggle, custom margins, per-page numbering)?  
Open an issue or send a note. Happy to iterate.
