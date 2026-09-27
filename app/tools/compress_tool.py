"""Compress PDF — reduce file size."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QComboBox

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops
from core.utils import human_size


class CompressTool(BaseTool):
    TITLE = "Compress PDF"
    DESCRIPTION = "Reduce the file size of a PDF for easier sharing."
    ICON = "📦"

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

        # Quality selector
        self.add_widget(self.make_field_label("COMPRESSION LEVEL"))
        self._quality = QComboBox()
        self._quality.addItems([
            "Screen  ·  Smallest file, lower quality",
            "Ebook  ·  Balanced",
            "Printer  ·  High quality",
            "Prepress  ·  Maximum quality",
        ])
        self._quality.setCurrentIndex(1)
        self.add_widget(self._quality)

        self.add_spacing(8)

        # Action
        self._btn = self.make_primary_btn("Compress & Save")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._compress)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    def _on_file(self, paths: list[str]):
        self._src = paths[0]
        size = human_size(Path(self._src).stat().st_size)
        count = pdf_ops.page_count(self._src)
        self._file_lbl.setText(f"📄  {Path(self._src).name}  ·  {count} pages  ·  {size}")
        self._file_lbl.show()
        self._drop.hide()
        self._btn.setEnabled(True)
        self.clear_status()

    def _compress(self):
        if not self._src:
            return
        dst = self.save_file_dialog()
        if not dst:
            return
        power = self._quality.currentIndex()
        try:
            pdf_ops.compress_pdf(self._src, dst, power)
            orig = Path(self._src).stat().st_size
            comp = Path(dst).stat().st_size
            pct = ((orig - comp) / orig) * 100 if orig > 0 else 0
            self.show_success(
                f"Compressed → {Path(dst).name}  ·  "
                f"{human_size(orig)} → {human_size(comp)}  ({pct:.0f}% smaller)"
            )
        except Exception as e:
            self.show_error(f"Failed: {e}")
