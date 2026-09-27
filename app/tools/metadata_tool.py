"""Metadata Editor — view and edit PDF document properties."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QLabel, QFormLayout, QFrame

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


class MetadataTool(BaseTool):
    TITLE = "Edit Metadata"
    DESCRIPTION = "View and update a PDF's title, author, subject, and keywords."
    ICON = "🏷️"

    FIELDS = [
        ("title", "TITLE"),
        ("author", "AUTHOR"),
        ("subject", "SUBJECT"),
        ("keywords", "KEYWORDS"),
        ("creator", "CREATOR"),
        ("producer", "PRODUCER"),
    ]

    def __init__(self):
        super().__init__()
        self._src: str | None = None
        self._inputs: dict[str, QLineEdit] = {}

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

        # Metadata form (hidden until file loaded)
        self._form_frame = QFrame()
        self._form_frame.setProperty("class", "card")
        form_layout = QFormLayout(self._form_frame)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(20, 20, 20, 20)

        for key, label_text in self.FIELDS:
            lbl = QLabel(label_text)
            lbl.setProperty("class", "field_label")
            inp = QLineEdit()
            inp.setPlaceholderText(f"Enter {label_text.lower()}")
            self._inputs[key] = inp
            form_layout.addRow(lbl, inp)

        self._form_frame.hide()
        self.add_widget(self._form_frame)

        self.add_spacing(8)

        # Action
        self._btn = self.make_primary_btn("Save Metadata")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._save)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    def _on_file(self, paths: list[str]):
        self._src = paths[0]
        self._file_lbl.setText(f"📄  {Path(self._src).name}")
        self._file_lbl.show()
        self._drop.hide()
        self._form_frame.show()
        self._btn.setEnabled(True)
        self.clear_status()

        # Load existing metadata
        try:
            meta = pdf_ops.read_metadata(self._src)
            for key, _ in self.FIELDS:
                self._inputs[key].setText(meta.get(key, ""))
        except Exception:
            pass  # If metadata can't be read, leave fields empty

    def _save(self):
        if not self._src:
            return
        meta = {key: self._inputs[key].text() for key, _ in self.FIELDS}
        dst = self.save_file_dialog()
        if not dst:
            return
        try:
            pdf_ops.write_metadata(self._src, dst, meta)
            self.show_success(f"Metadata updated → {Path(dst).name}")
        except Exception as e:
            self.show_error(f"Failed: {e}")
