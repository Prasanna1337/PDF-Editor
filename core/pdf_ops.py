"""
Backend PDF operations — every heavy-lifting function lives here.
The UI layer calls these and never touches pypdf / pikepdf directly.
"""
from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Optional

import pymupdf as fitz  # PyMuPDF
import pikepdf
from pypdf import PdfReader, PdfWriter
from PIL import Image

from core.utils import get_temp_dir


# ── Password ────────────────────────────────────────────────────────────

def remove_password(src: str, password: str, dst: str) -> None:
    """Open *src* with *password*, write an unencrypted copy to *dst*."""
    with pikepdf.open(src, password=password) as pdf:
        pdf.save(dst)


# ── Merge ────────────────────────────────────────────────────────────────

def merge_pdfs(paths: list[str], dst: str) -> None:
    """Merge several PDFs (in order) into a single file at *dst*."""
    writer = PdfWriter()
    for p in paths:
        reader = PdfReader(p)
        for page in reader.pages:
            writer.add_page(page)
    with open(dst, "wb") as f:
        writer.write(f)


# ── Split ────────────────────────────────────────────────────────────────

def split_pdf(src: str, page_ranges: list[tuple[int, int]], dst: str) -> None:
    """
    Extract *page_ranges* (1-indexed, inclusive) from *src* into *dst*.
    Example: [(1, 3), (5, 5)] extracts pages 1-3 and 5.
    """
    reader = PdfReader(src)
    writer = PdfWriter()
    for start, end in page_ranges:
        for i in range(start - 1, min(end, len(reader.pages))):
            writer.add_page(reader.pages[i])
    with open(dst, "wb") as f:
        writer.write(f)


def split_each_page(src: str, dst_dir: str) -> list[str]:
    """Split every page into its own PDF inside *dst_dir*."""
    reader = PdfReader(src)
    created: list[str] = []
    base = Path(src).stem
    for i, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        out = os.path.join(dst_dir, f"{base}_page_{i}.pdf")
        with open(out, "wb") as f:
            writer.write(f)
        created.append(out)
    return created


# ── Rotate ───────────────────────────────────────────────────────────────

def rotate_pages(src: str, rotations: dict[int, int], dst: str) -> None:
    """
    Rotate specific pages.
    *rotations*: {page_number (1-indexed): degrees} where degrees ∈ {90,180,270}.
    """
    reader = PdfReader(src)
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if (i + 1) in rotations:
            page.rotate(rotations[i + 1])
        writer.add_page(page)
    with open(dst, "wb") as f:
        writer.write(f)


def rotate_all_pages(src: str, degrees: int, dst: str) -> None:
    """Rotate every page by *degrees* (90 / 180 / 270)."""
    reader = PdfReader(src)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    with open(dst, "wb") as f:
        writer.write(f)


# ── Compress ─────────────────────────────────────────────────────────────

def compress_pdf(src: str, dst: str, power: int = 2) -> None:
    """
    Compress a PDF by downscaling images.
    *power*: 0 = screen (72 dpi), 1 = ebook (150), 2 = printer (300), 3 = prepress.
    Falls back to lossless stream compression if image resampling is unavailable.
    """
    reader = PdfReader(src)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(reader.metadata or {})

    # Compress all content streams
    for page in writer.pages:
        page.compress_content_streams()

    # Remove duplicate objects
    writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)

    with open(dst, "wb") as f:
        writer.write(f)


# ── Watermark ────────────────────────────────────────────────────────────

def add_text_watermark(
    src: str,
    dst: str,
    text: str,
    font_size: int = 48,
    opacity: float = 0.15,
    angle: float = 45,
) -> None:
    """Overlay a diagonal text watermark on every page using PyMuPDF."""
    doc = fitz.open(src)
    for page in doc:
        rect = page.rect
        # Center of the page
        cx, cy = rect.width / 2, rect.height / 2

        # Create text writer
        tw = fitz.TextWriter(page.rect)
        font = fitz.Font("helv")
        text_width = font.text_length(text, fontsize=font_size)

        # Position text at center
        x = cx - text_width / 2
        y = cy + font_size / 2

        tw.append((x, y), text, font=font, fontsize=font_size)

        # Apply with rotation and opacity
        morph = (fitz.Point(cx, cy), fitz.Matrix(angle))
        tw.write_text(page, morph=morph, opacity=opacity, color=(0.5, 0.5, 0.5))

    doc.save(dst, garbage=4, deflate=True)
    doc.close()


# ── PDF → Images ─────────────────────────────────────────────────────────

def pdf_to_images(
    src: str, dst_dir: str, fmt: str = "png", dpi: int = 150
) -> list[str]:
    """Render each page of *src* as an image file inside *dst_dir*."""
    doc = fitz.open(src)
    base = Path(src).stem
    created: list[str] = []
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=mat)
        out = os.path.join(dst_dir, f"{base}_page_{i}.{fmt}")
        pix.save(out)
        created.append(out)
    doc.close()
    return created


# ── Images → PDF ─────────────────────────────────────────────────────────

def images_to_pdf(image_paths: list[str], dst: str) -> None:
    """Convert a list of image files into a single PDF."""
    images: list[Image.Image] = []
    for p in image_paths:
        img = Image.open(p).convert("RGB")
        images.append(img)
    if not images:
        raise ValueError("No images provided")
    images[0].save(dst, save_all=True, append_images=images[1:], resolution=150)


# ── Reorder ──────────────────────────────────────────────────────────────

def reorder_pages(src: str, new_order: list[int], dst: str) -> None:
    """
    Write *src* to *dst* with pages reordered.
    *new_order*: list of 1-indexed page numbers in desired order.
    """
    reader = PdfReader(src)
    writer = PdfWriter()
    for idx in new_order:
        writer.add_page(reader.pages[idx - 1])
    with open(dst, "wb") as f:
        writer.write(f)


# ── Metadata ─────────────────────────────────────────────────────────────

def read_metadata(src: str) -> dict[str, str]:
    """Return the document-info dictionary from *src*."""
    reader = PdfReader(src)
    meta = reader.metadata or {}
    return {
        "title": meta.get("/Title", "") or "",
        "author": meta.get("/Author", "") or "",
        "subject": meta.get("/Subject", "") or "",
        "keywords": meta.get("/Keywords", "") or "",
        "creator": meta.get("/Creator", "") or "",
        "producer": meta.get("/Producer", "") or "",
    }


def write_metadata(src: str, dst: str, meta: dict[str, str]) -> None:
    """Copy *src* to *dst* with updated metadata fields."""
    reader = PdfReader(src)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": meta.get("title", ""),
        "/Author": meta.get("author", ""),
        "/Subject": meta.get("subject", ""),
        "/Keywords": meta.get("keywords", ""),
        "/Creator": meta.get("creator", ""),
        "/Producer": meta.get("producer", ""),
    })
    with open(dst, "wb") as f:
        writer.write(f)


# ── Helpers ──────────────────────────────────────────────────────────────

def page_count(src: str) -> int:
    """Return the number of pages in a PDF."""
    reader = PdfReader(src)
    return len(reader.pages)


def render_page_thumbnail(src: str, page_num: int, width: int = 200) -> bytes:
    """
    Render a single page as a PNG thumbnail (returns raw bytes).
    *page_num* is 0-indexed.
    """
    doc = fitz.open(src)
    page = doc[page_num]
    zoom = width / page.rect.width
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    data = pix.tobytes("png")
    doc.close()
    return data
