"""Merge PDFs — combine multiple files into one."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout,
)

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class MergeTool(BaseTool):
    TITLE = "Merge PDFs"
    DESCRIPTION = "Combine multiple PDF files into a single document. Drag to reorder."
    ICON = "📑"

    def __init__(self):
        super().__init__()
        self._paths: list[str] = []

        # Drop zone
        self._drop = DropZone(
            label="Drop PDF files here",
            hint="or click to browse · multiple files supported",
            multi=True,
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
        self._add_btn = self.make_secondary_btn("+ Add more files")
        self._add_btn.clicked.connect(lambda: self._drop._browse())
        self._add_btn.hide()

        self._clear_btn = self.make_secondary_btn("Clear all")
        self._clear_btn.clicked.connect(self._clear)
        self._clear_btn.hide()

        ctrl_row = self.make_row(self._add_btn, self._clear_btn, 1)
        self.add_layout(ctrl_row)

        self.add_spacing(8)

        # Merge button
        self._btn = self.make_primary_btn("Merge into one PDF")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._merge)
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
        self._btn.setEnabled(len(self._paths) >= 2)
        self.clear_status()

    def _clear(self):
        self._paths.clear()
        self._list.clear()
        self._drop.show()
        self._update_ui()

    def _merge(self):
        # Respect visual order (user may have dragged to reorder)
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
            pdf_ops.merge_pdfs(ordered, dst)
            self.show_success(f"Merged {len(ordered)} files → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")
