# 📜 Scribe

A minimal, offline PDF workbench. Clean dark interface, fast, private, and portable. No complicated setup — works on Windows, macOS, and Linux.

---

## ⬇️ Download & Run (Quick Start)

### Step 1 — Install Python
If you don't have Python, download and install it from:
👉 **https://www.python.org/downloads/**

> ⚠️ During installation, make sure to check **"Add Python to PATH"**

### Step 2 — Download this project
Click the green **`< > Code`** button on this page → **Download ZIP** → Extract it anywhere on your PC.

Or if you have Git:
```bash
git clone https://github.com/Prasanna1337/PDF-Editor.git
cd PDF-Editor
```

### Step 3 — Install dependencies
Open a terminal / command prompt inside the extracted folder and run:
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
python main.py
```

The **Scribe** window will open. That's it! 🎉

---

## 🛠️ Features

| Tool | Description |
|------|-------------|
| 🔓 Remove Password | Batch unlock multiple password-protected PDFs with one password |
| 📑 Merge PDFs | Combine multiple PDFs into one, drag to reorder |
| ✂️ Split PDF | Extract specific pages or split into individual files |
| 🔄 Rotate Pages | Rotate all pages 90°/180°/270° |
| 📦 Compress | Reduce file size with quality presets |
| 💧 Watermark | Add diagonal text watermark with opacity control |
| 🖼️ PDF → Images | Export pages as PNG/JPG at custom DPI |
| 📷 Images → PDF | Convert image collections into a PDF |
| ↕️ Reorder Pages | Drag-and-drop thumbnail reordering |
| 🏷️ Edit Metadata | Edit title, author, subject, keywords |

---

## 🖥️ System Requirements

| | Minimum |
|--|---------|
| OS | Windows 10/11 · macOS 12+ · Ubuntu 20.04+ |
| Python | 3.10 or newer |
| RAM | 256 MB |
| Disk | 200 MB (for dependencies) |

---

## ❓ Troubleshooting

**`pip` not found?**
Try `pip3` instead of `pip`, or run `python -m pip install -r requirements.txt`.

**`python` not found?**
Make sure you checked "Add Python to PATH" during installation. Restart your terminal and try again.

**App doesn't open?**
Make sure all dependencies installed successfully (no red errors during Step 3).

---

## 🏗️ Build a Portable .exe (Windows)

If you want a single `.exe` file that needs no Python:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon="app_icon.ico" --add-data="app_icon.ico;." --name="Scribe" main.py
```
The output will be in `dist/Scribe.exe`.

---

## 📁 Project Structure

```
PDF-Editor/
├── main.py              # Entry point — run this
├── requirements.txt     # Python dependencies
├── app/
│   ├── window.py        # Main window & sidebar navigation
│   ├── theme.py         # Dark theme stylesheet
│   ├── widgets/
│   │   └── drop_zone.py # Drag-and-drop file input
│   └── tools/           # One file per tool (10 tools)
│       ├── password_tool.py
│       ├── merge_tool.py
│       ├── split_tool.py
│       ├── rotate_tool.py
│       ├── compress_tool.py
│       ├── watermark_tool.py
│       ├── pdf_to_img.py
│       ├── img_to_pdf.py
│       ├── reorder_tool.py
│       └── metadata_tool.py
└── core/
    ├── pdf_ops.py       # All PDF manipulation logic
    └── utils.py         # File helpers
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `PyQt6` | GUI framework |
| `pypdf` | PDF reading & writing |
| `pikepdf` | Password removal & encryption |
| `PyMuPDF` | Page thumbnails & image export |
| `Pillow` | Image processing |

---

## 📄 License

MIT — free to use, modify, and distribute.
