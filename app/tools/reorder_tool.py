"""Reorder Pages — drag-and-drop page reordering via thumbnail list."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QLabel

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class ReorderTool(BaseTool):
    TITLE = "Reorder Pages"
    DESCRIPTION = "Drag and drop to rearrange the pages in your PDF."
    ICON = "↕️"

    def __init__(self):
        super().__init__()
        self._src: str | None = None
        self._page_count = 0

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

        # Page list with thumbnails
        self._list = QListWidget()
        self._list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self._list.setIconSize(QSize(60, 80))
        self._list.setMinimumHeight(300)
        self._list.hide()
        self.add_widget(self._list)

        self.add_spacing(8)

        # Action
        self._btn = self.make_primary_btn("Save Reordered PDF")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._save)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    def _on_file(self, paths: list[str]):
        self._src = paths[0]
        self._page_count = pdf_ops.page_count(self._src)
        self._file_lbl.setText(
            f"📄  {Path(self._src).name}  ·  {self._page_count} pages"
        )
        self._file_lbl.show()
        self._drop.hide()
        self._list.show()
        self._btn.setEnabled(True)
        self.clear_status()

        # Load thumbnails
        self._list.clear()
        for i in range(self._page_count):
            thumb_data = pdf_ops.render_page_thumbnail(self._src, i, width=60)
            pix = QPixmap()
            pix.loadFromData(thumb_data)
            item = QListWidgetItem(QIcon(pix), f"  Page {i + 1}")
            item.setData(Qt.ItemDataRole.UserRole, i + 1)  # 1-indexed
            self._list.addItem(item)

    def _save(self):
        if not self._src:
            return
        # Get current visual order
        order = []
        for i in range(self._list.count()):
            order.append(self._list.item(i).data(Qt.ItemDataRole.UserRole))
        dst = self.save_file_dialog()
        if not dst:
            return
        try:
            pdf_ops.reorder_pages(self._src, order, dst)
            self.show_success(f"Reordered PDF saved → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")
