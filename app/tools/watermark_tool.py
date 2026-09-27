"""Watermark — add text watermark to every page."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QLabel, QSpinBox, QSlider, QHBoxLayout

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class WatermarkTool(BaseTool):
    TITLE = "Add Watermark"
    DESCRIPTION = "Overlay a text watermark diagonally across every page."
    ICON = "💧"

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

        # Watermark text
        self.add_widget(self.make_field_label("WATERMARK TEXT"))
        self._text = QLineEdit()
        self._text.setPlaceholderText("e.g. CONFIDENTIAL")
        self.add_widget(self._text)

        self.add_spacing(8)

        # Font size
        self.add_widget(self.make_field_label("FONT SIZE"))
        self._fontsize = QSpinBox()
        self._fontsize.setRange(12, 200)
        self._fontsize.setValue(48)
        self.add_widget(self._fontsize)

        self.add_spacing(8)

        # Opacity
        self.add_widget(self.make_field_label("OPACITY"))
        opacity_row = QHBoxLayout()
        opacity_row.setSpacing(12)
        self._opacity = QSlider(Qt.Orientation.Horizontal)
        self._opacity.setRange(5, 80)
        self._opacity.setValue(15)
        self._opacity_lbl = QLabel("15%")
        self._opacity.valueChanged.connect(lambda v: self._opacity_lbl.setText(f"{v}%"))
        opacity_row.addWidget(self._opacity)
        opacity_row.addWidget(self._opacity_lbl)
        self.add_layout(opacity_row)

        self.add_spacing(8)

        # Action
        self._btn = self.make_primary_btn("Apply Watermark")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._apply)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    def _on_file(self, paths: list[str]):
        self._src = paths[0]
        self._file_lbl.setText(f"📄  {Path(self._src).name}")
        self._file_lbl.show()
        self._drop.hide()
        self._btn.setEnabled(True)
        self.clear_status()

    def _apply(self):
        if not self._src:
            return
        text = self._text.text().strip()
        if not text:
            self.show_error("Enter watermark text.")
            return
        dst = self.save_file_dialog()
        if not dst:
            return
        try:
            pdf_ops.add_text_watermark(
                self._src, dst, text,
                font_size=self._fontsize.value(),
                opacity=self._opacity.value() / 100,
            )
            self.show_success(f"Watermark applied → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")
