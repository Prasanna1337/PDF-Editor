"""
DropZone — a drag-and-drop area for selecting files.
Supports single or multi-file mode and file-type filtering.
"""
from __future__ import annotations

import os
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QPushButton,
    QSizePolicy,
)


class DropZone(QFrame):
    """Drag-and-drop file selector widget."""

    files_dropped = pyqtSignal(list)  # emits list[str]

    def __init__(
        self,
        accept: str = "PDF Files (*.pdf)",
        multi: bool = False,
        label: str = "Drop your PDF here",
        hint: str = "or click to browse files",
        parent=None,
    ):
        super().__init__(parent)
        self.setObjectName("drop_zone")
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._accept = accept
        self._multi = multi

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)
        layout.setContentsMargins(32, 32, 32, 32)

        self._icon = QLabel("📄")
        self._icon.setObjectName("drop_zone_icon")
        self._icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel(label)
        self._label.setObjectName("drop_zone_text")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._hint = QLabel(hint)
        self._hint.setObjectName("drop_zone_hint")
        self._hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self._icon)
        layout.addWidget(self._label)
        layout.addWidget(self._hint)

    # -- events ---

    def mousePressEvent(self, event):
        self._browse()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragover", True)
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("dragover", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def dropEvent(self, event):
        self.setProperty("dragover", False)
        self.style().unpolish(self)
        self.style().polish(self)
        urls = event.mimeData().urls()
        paths = [u.toLocalFile() for u in urls if os.path.isfile(u.toLocalFile())]
        if paths:
            if not self._multi:
                paths = paths[:1]
            self.files_dropped.emit(paths)

    # -- internals ---

    def _browse(self):
        if self._multi:
            paths, _ = QFileDialog.getOpenFileNames(
                self, "Select files", "", self._accept
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self, "Select file", "", self._accept
            )
            paths = [path] if path else []
        if paths:
            self.files_dropped.emit(paths)

    def set_label(self, text: str):
        self._label.setText(text)

    def set_icon(self, icon: str):
        self._icon.setText(icon)
