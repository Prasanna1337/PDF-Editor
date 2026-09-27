"""
BaseTool — abstract base class for every tool page.
Provides consistent layout: title, description, content area, and status bar.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame,
    QScrollArea, QSizePolicy, QPushButton, QFileDialog,
)

from app import theme


class BaseTool(QScrollArea):
    """Base class every tool page inherits from."""

    TITLE: str = "Tool"
    DESCRIPTION: str = ""
    ICON: str = "📄"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("tool_page")
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Container
        container = QWidget()
        self._layout = QVBoxLayout(container)
        self._layout.setContentsMargins(48, 40, 48, 40)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        title = QLabel(self.TITLE)
        title.setObjectName("tool_title")

        desc = QLabel(self.DESCRIPTION)
        desc.setObjectName("tool_desc")
        desc.setWordWrap(True)

        self._layout.addWidget(title)
        self._layout.addSpacing(6)
        self._layout.addWidget(desc)
        self._layout.addSpacing(28)

        # Content area — subclasses add widgets here
        self._content = QVBoxLayout()
        self._content.setSpacing(16)
        self._layout.addLayout(self._content)

        # Status label (hidden by default)
        self._layout.addSpacing(20)
        self._status = QLabel("")
        self._status.setWordWrap(True)
        self._status.hide()
        self._layout.addWidget(self._status)

        self._layout.addStretch()
        self.setWidget(container)

    # ── Helpers for subclasses ──

    def add_widget(self, w: QWidget):
        """Append a widget to the content area."""
        self._content.addWidget(w)

    def add_layout(self, lay):
        """Append a layout to the content area."""
        self._content.addLayout(lay)

    def add_spacing(self, px: int = 12):
        self._content.addSpacing(px)

    def add_separator(self):
        sep = QFrame()
        sep.setProperty("class", "separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        self._content.addWidget(sep)

    def show_success(self, msg: str):
        self._status.setProperty("class", "status_success")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._status.setText(f"✓  {msg}")
        self._status.show()

    def show_error(self, msg: str):
        self._status.setProperty("class", "status_error")
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
        self._status.setText(f"✕  {msg}")
        self._status.show()

    def clear_status(self):
        self._status.hide()
        self._status.setText("")

    def make_primary_btn(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", "primary")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def make_secondary_btn(self, text: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", "secondary")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def save_file_dialog(self, title: str = "Save PDF", filter: str = "PDF Files (*.pdf)") -> str:
        path, _ = QFileDialog.getSaveFileName(self, title, "", filter)
        return path

    def make_field_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setProperty("class", "field_label")
        return lbl

    def make_row(self, *widgets) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)
        for w in widgets:
            if isinstance(w, QWidget):
                row.addWidget(w)
            elif isinstance(w, int):
                row.addStretch(w)
        return row
