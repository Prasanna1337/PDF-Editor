"""
Utility helpers — file handling, temp dirs, error formatting.
"""
import os
import tempfile
from pathlib import Path


def get_temp_dir() -> Path:
    """Return a persistent temp directory for intermediate files."""
    d = Path(tempfile.gettempdir()) / "pdf_editor_tmp"
    d.mkdir(exist_ok=True)
    return d


def human_size(nbytes: int) -> str:
    """Convert byte count to a human-readable string."""
    for unit in ("B", "KB", "MB", "GB"):
        if abs(nbytes) < 1024:
            return f"{nbytes:.1f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.1f} TB"


def safe_filename(name: str) -> str:
    """Strip characters that are invalid in Windows file names."""
    for ch in r'<>:"/\|?*':
        name = name.replace(ch, "_")
    return name.strip()


def file_ext(path: str) -> str:
    """Return the lowercase file extension including the dot."""
    return os.path.splitext(path)[1].lower()


def is_pdf(path: str) -> bool:
    """Check whether a path points to a PDF file."""
    return file_ext(path) == ".pdf"


def is_image(path: str) -> bool:
    """Check whether a path points to a common image file."""
    return file_ext(path) in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")
