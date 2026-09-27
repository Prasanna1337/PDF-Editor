# 📄 PDF Editor

A minimal, portable all-in-one PDF utility for Windows. No installation needed — just run the `.exe`.

## Features

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

## Tech Stack

- **GUI**: PyQt6
- **PDF Engine**: `pypdf` + `pikepdf` + `PyMuPDF`
- **Image**: Pillow
- **Bundling**: PyInstaller (single portable `.exe`)

## Run from Source

```bash
# Install dependencies
pip install -r requirements.txt

# Launch
python main.py
```

## Build Portable .exe

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="PDF Editor" main.py
# Output: dist/PDF Editor.exe
```

## Project Structure

```
pdf-editor/
├── main.py              # Entry point
├── app/
│   ├── window.py        # Main window & sidebar navigation
│   ├── theme.py         # Dark theme QSS stylesheet
│   ├── widgets/
│   │   └── drop_zone.py # Drag-and-drop file input widget
│   └── tools/           # One file per tool (10 tools)
└── core/
    ├── pdf_ops.py       # All PDF manipulation logic
    └── utils.py         # File helpers
```

## License

MIT
