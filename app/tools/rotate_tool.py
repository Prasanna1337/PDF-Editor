"""Rotate Pages — rotate all or individual pages by 90°/180°/270°."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QComboBox, QHBoxLayout

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class RotateTool(BaseTool):
    TITLE = "Rotate Pages"
    DESCRIPTION = "Rotate all pages in a PDF by a chosen angle."
    ICON = "🔄"

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

        # Angle selector
        self.add_widget(self.make_field_label("ROTATION ANGLE"))
        self._angle = QComboBox()
        self._angle.addItems(["90° Clockwise", "180°", "90° Counter-clockwise"])
        self._angle_map = {0: 90, 1: 180, 2: 270}
        self.add_widget(self._angle)

        self.add_spacing(8)

        # Action
        self._btn = self.make_primary_btn("Rotate & Save")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._rotate)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    def _on_file(self, paths: list[str]):
        self._src = paths[0]
        count = pdf_ops.page_count(self._src)
        self._file_lbl.setText(f"📄  {Path(self._src).name}  ·  {count} pages")
        self._file_lbl.show()
        self._drop.hide()
        self._btn.setEnabled(True)
        self.clear_status()

    def _rotate(self):
        if not self._src:
            return
        degrees = self._angle_map[self._angle.currentIndex()]
        dst = self.save_file_dialog()
        if not dst:
            return
        try:
            pdf_ops.rotate_all_pages(self._src, degrees, dst)
            self.show_success(f"Rotated {degrees}° → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")
