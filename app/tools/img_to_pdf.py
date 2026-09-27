"""Images to PDF — convert a batch of images into a single PDF."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidget, QPushButton

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class ImgToPdfTool(BaseTool):
    TITLE = "Images to PDF"
    DESCRIPTION = "Convert a collection of images into a single PDF document."
    ICON = "📷"

    def __init__(self):
        super().__init__()
        self._paths: list[str] = []

        # Drop zone
        self._drop = DropZone(
            accept="Images (*.png *.jpg *.jpeg *.bmp *.tiff *.webp)",
            multi=True,
            label="Drop images here",
            hint="PNG, JPG, BMP, TIFF, WebP supported",
        )
        self._drop.files_dropped.connect(self._on_files)
        self.add_widget(self._drop)

        # File list
        self._list = QListWidget()
        self._list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self._list.setMinimumHeight(120)
        self._list.hide()
        self.add_widget(self._list)

        # Controls
        self._add_btn = self.make_secondary_btn("+ Add more images")
        self._add_btn.clicked.connect(lambda: self._drop._browse())
        self._add_btn.hide()

        self._clear_btn = self.make_secondary_btn("Clear all")
        self._clear_btn.clicked.connect(self._clear)
        self._clear_btn.hide()

        ctrl_row = self.make_row(self._add_btn, self._clear_btn, 1)
        self.add_layout(ctrl_row)

        self.add_spacing(8)

        # Convert button
        self._btn = self.make_primary_btn("Convert to PDF")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._convert)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    def _on_files(self, paths: list[str]):
        for p in paths:
            if p not in self._paths:
                self._paths.append(p)
                self._list.addItem(Path(p).name)
        self._update_ui()

    def _update_ui(self):
        has = len(self._paths) > 0
        self._list.setVisible(has)
        self._add_btn.setVisible(has)
        self._clear_btn.setVisible(has)
        self._btn.setEnabled(has)
        self.clear_status()

    def _clear(self):
        self._paths.clear()
        self._list.clear()
        self._drop.show()
        self._update_ui()

    def _convert(self):
        if not self._paths:
            return
        # Respect visual order
        ordered = []
        for i in range(self._list.count()):
            name = self._list.item(i).text()
            for p in self._paths:
                if Path(p).name == name and p not in ordered:
                    ordered.append(p)
                    break
        dst = self.save_file_dialog()
        if not dst:
            return
        try:
            pdf_ops.images_to_pdf(ordered, dst)
            self.show_success(f"Created PDF with {len(ordered)} pages → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")
