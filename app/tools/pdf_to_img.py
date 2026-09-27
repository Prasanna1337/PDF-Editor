"""PDF to Images — export each page as PNG/JPG."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QComboBox, QSpinBox, QFileDialog

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class PdfToImgTool(BaseTool):
    TITLE = "PDF to Images"
    DESCRIPTION = "Export every page as a high-quality image file."
    ICON = "🖼️"

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

        # Format
        self.add_widget(self.make_field_label("IMAGE FORMAT"))
        self._fmt = QComboBox()
        self._fmt.addItems(["PNG", "JPEG"])
        self.add_widget(self._fmt)

        self.add_spacing(8)

        # DPI
        self.add_widget(self.make_field_label("RESOLUTION (DPI)"))
        self._dpi = QSpinBox()
        self._dpi.setRange(72, 600)
        self._dpi.setValue(150)
        self._dpi.setSingleStep(50)
        self.add_widget(self._dpi)

        self.add_spacing(8)

        # Action
        self._btn = self.make_primary_btn("Export Images")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._export)
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

    def _export(self):
        if not self._src:
            return
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if not folder:
            return
        fmt = self._fmt.currentText().lower()
        if fmt == "jpeg":
            fmt = "jpg"
        try:
            created = pdf_ops.pdf_to_images(self._src, folder, fmt, self._dpi.value())
            self.show_success(f"Exported {len(created)} images to folder")
        except Exception as e:
            self.show_error(f"Failed: {e}")
