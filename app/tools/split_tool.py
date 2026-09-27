"""Split PDF — extract specific pages or split into individual pages."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QLabel, QHBoxLayout, QFileDialog

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class SplitTool(BaseTool):
    TITLE = "Split PDF"
    DESCRIPTION = "Extract specific pages or split every page into separate files."
    ICON = "✂️"

    def __init__(self):
        super().__init__()
        self._src: str | None = None

        # Drop zone
        self._drop = DropZone(label="Drop your PDF here")
        self._drop.files_dropped.connect(self._on_file)
        self.add_widget(self._drop)

        # File indicator
        self._file_lbl = QLabel("")
        self._file_lbl.setProperty("class", "file_label")
        self._file_lbl.hide()
        self.add_widget(self._file_lbl)

        self.add_spacing(8)

        # Page range input
        self.add_widget(self.make_field_label("PAGE RANGE"))
        self._range = QLineEdit()
        self._range.setPlaceholderText("e.g. 1-3, 5, 8-10  (leave empty to split all pages)")
        self.add_widget(self._range)

        self.add_spacing(8)

        # Actions
        self._extract_btn = self.make_primary_btn("Extract pages")
        self._extract_btn.setEnabled(False)
        self._extract_btn.clicked.connect(self._extract)

        self._split_btn = self.make_secondary_btn("Split every page")
        self._split_btn.setEnabled(False)
        self._split_btn.clicked.connect(self._split_all)

        row = self.make_row(1, self._split_btn, self._extract_btn)
        self.add_layout(row)

    def _on_file(self, paths: list[str]):
        self._src = paths[0]
        count = pdf_ops.page_count(self._src)
        self._file_lbl.setText(f"📄  {Path(self._src).name}  ·  {count} pages")
        self._file_lbl.show()
        self._drop.hide()
        self._extract_btn.setEnabled(True)
        self._split_btn.setEnabled(True)
        self.clear_status()

    def _parse_ranges(self) -> list[tuple[int, int]]:
        text = self._range.text().strip()
        if not text:
            return []
        ranges = []
        for part in text.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-", 1)
                ranges.append((int(a.strip()), int(b.strip())))
            else:
                n = int(part)
                ranges.append((n, n))
        return ranges

    def _extract(self):
        if not self._src:
            return
        ranges = self._parse_ranges()
        if not ranges:
            self.show_error("Enter a page range like: 1-3, 5, 8-10")
            return
        dst = self.save_file_dialog()
        if not dst:
            return
        try:
            pdf_ops.split_pdf(self._src, ranges, dst)
            self.show_success(f"Extracted pages → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")

    def _split_all(self):
        if not self._src:
            return
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not folder:
            return
        try:
            created = pdf_ops.split_each_page(self._src, folder)
            self.show_success(f"Split into {len(created)} files")
        except Exception as e:
            self.show_error(f"Failed: {e}")
