"""Password Remover — unlock multiple password-protected PDFs at once."""
from __future__ import annotations

import os
from pathlib import Path

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QLineEdit, QLabel, QHBoxLayout, QListWidget, QListWidgetItem,
    QFileDialog, QProgressBar, QFrame,
)

from app.tools.base_tool import BaseTool
from app.widgets.drop_zone import DropZone
from core import pdf_ops


# ── Background worker ────────────────────────────────────────────────────

class UnlockWorker(QThread):
    """Unlocks PDFs on a background thread, reporting progress per file."""
    progress = pyqtSignal(int, str, bool)   # (index, message, ok)
    finished = pyqtSignal(int, int)          # (success_count, fail_count)

    def __init__(self, paths: list[str], password: str, out_dir: str):
        super().__init__()
        self._paths = paths
        self._password = password
        self._out_dir = out_dir

    def run(self):
        ok = fail = 0
        for i, src in enumerate(self._paths):
            stem = Path(src).stem
            dst = os.path.join(self._out_dir, f"{stem}_unlocked.pdf")
            try:
                pdf_ops.remove_password(src, self._password, dst)
                self.progress.emit(i, Path(src).name, True)
                ok += 1
            except Exception as exc:
                self.progress.emit(i, f"{Path(src).name} — {exc}", False)
                fail += 1
        self.finished.emit(ok, fail)


# ── Tool page ─────────────────────────────────────────────────────────────

class PasswordTool(BaseTool):
    TITLE = "Remove Password"
    DESCRIPTION = (
        "Import multiple locked PDFs, enter a single password, "
        "and save unlocked copies to a folder."
    )
    ICON = "🔓"

    def __init__(self):
        super().__init__()
        self._paths: list[str] = []
        self._worker: UnlockWorker | None = None

        # ── Drop zone ──
        self._drop = DropZone(
            label="Drop locked PDF files here",
            hint="or click to browse · multiple files supported",
            multi=True,
        )
        self._drop.files_dropped.connect(self._on_files)
        self.add_widget(self._drop)

        # ── File list ──
        self._list = QListWidget()
        self._list.setMinimumHeight(140)
        self._list.setMaximumHeight(260)
        self._list.hide()
        self.add_widget(self._list)

        # ── File list controls ──
        self._add_btn = self.make_secondary_btn("+ Add more files")
        self._add_btn.clicked.connect(lambda: self._drop._browse())
        self._add_btn.hide()

        self._clear_btn = self.make_secondary_btn("Clear all")
        self._clear_btn.clicked.connect(self._clear)
        self._clear_btn.hide()

        ctrl_row = self.make_row(self._add_btn, self._clear_btn, 1)
        self.add_layout(ctrl_row)

        self.add_spacing(8)

        # ── Password field ──
        self.add_widget(self.make_field_label("PASSWORD  (applied to all files)"))
        pw_row = QHBoxLayout()
        pw_row.setSpacing(8)
        self._pw = QLineEdit()
        self._pw.setPlaceholderText("Enter the shared password")
        self._pw.setEchoMode(QLineEdit.EchoMode.Password)

        self._toggle_btn = self.make_secondary_btn("Show")
        self._toggle_btn.setFixedWidth(64)
        self._toggle_btn.clicked.connect(self._toggle_pw)

        pw_row.addWidget(self._pw)
        pw_row.addWidget(self._toggle_btn)
        self.add_layout(pw_row)

        self.add_spacing(8)

        # ── Output folder ──
        self.add_widget(self.make_field_label("OUTPUT FOLDER"))
        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        self._folder_lbl = QLabel("Same folder as each source file")
        self._folder_lbl.setProperty("class", "file_label")
        self._folder_lbl.setMinimumWidth(1)

        self._folder_btn = self.make_secondary_btn("Choose…")
        self._folder_btn.setFixedWidth(80)
        self._folder_btn.clicked.connect(self._choose_folder)

        self._reset_folder_btn = self.make_secondary_btn("Reset")
        self._reset_folder_btn.setFixedWidth(60)
        self._reset_folder_btn.clicked.connect(self._reset_folder)
        self._reset_folder_btn.hide()

        folder_row.addWidget(self._folder_lbl, 1)
        folder_row.addWidget(self._folder_btn)
        folder_row.addWidget(self._reset_folder_btn)
        self.add_layout(folder_row)
        self._out_dir: str | None = None   # None = same dir as source

        self.add_spacing(8)

        # ── Progress bar (hidden until processing) ──
        self._progress = QProgressBar()
        self._progress.hide()
        self.add_widget(self._progress)

        # ── Unlock button ──
        self._btn = self.make_primary_btn("🔓  Unlock All PDFs")
        self._btn.setEnabled(False)
        self._btn.clicked.connect(self._unlock_all)
        row = self.make_row(1, self._btn)
        self.add_layout(row)

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_files(self, paths: list[str]):
        added = 0
        for p in paths:
            if p not in self._paths:
                self._paths.append(p)
                item = QListWidgetItem(f"  📄  {Path(p).name}")
                item.setToolTip(p)
                self._list.addItem(item)
                added += 1
        if added:
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

    def _toggle_pw(self):
        hidden = self._pw.echoMode() == QLineEdit.EchoMode.Password
        self._pw.setEchoMode(
            QLineEdit.EchoMode.Normal if hidden else QLineEdit.EchoMode.Password
        )
        self._toggle_btn.setText("Hide" if hidden else "Show")

    def _choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder:
            self._out_dir = folder
            self._folder_lbl.setText(folder)
            self._reset_folder_btn.show()

    def _reset_folder(self):
        self._out_dir = None
        self._folder_lbl.setText("Same folder as each source file")
        self._reset_folder_btn.hide()

    # ── Unlock logic ──────────────────────────────────────────────────────

    def _unlock_all(self):
        if not self._paths:
            self.show_error("Add at least one PDF file.")
            return
        pw = self._pw.text()
        if not pw:
            self.show_error("Enter the password.")
            return

        # Determine effective output dir
        # If no folder chosen we'll pass a sentinel; worker handles per-file dir
        out_dir = self._out_dir or ""

        # Lock UI
        self._btn.setEnabled(False)
        self._add_btn.setEnabled(False)
        self._clear_btn.setEnabled(False)
        self._pw.setEnabled(False)

        # Reset list icons
        for i in range(self._list.count()):
            item = self._list.item(i)
            item.setText(f"  📄  {Path(self._paths[i]).name}")

        # Progress
        self._progress.setMaximum(len(self._paths))
        self._progress.setValue(0)
        self._progress.show()
        self.clear_status()

        # Start worker (using sentinel "" means use source file's own dir)
        self._worker = _MultiUnlockWorker(self._paths, pw, out_dir)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.start()

    def _on_progress(self, index: int, name: str, ok: bool):
        item = self._list.item(index)
        if ok:
            item.setText(f"  ✅  {Path(self._paths[index]).name}")
        else:
            item.setText(f"  ❌  {name}")
        self._progress.setValue(index + 1)

    def _on_finished(self, ok: int, fail: int):
        # Unlock UI
        self._btn.setEnabled(True)
        self._add_btn.setEnabled(True)
        self._clear_btn.setEnabled(True)
        self._pw.setEnabled(True)
        self._progress.hide()

        if fail == 0:
            self.show_success(f"All {ok} files unlocked successfully.")
        elif ok == 0:
            self.show_error(f"All {fail} files failed — check the password.")
        else:
            self.show_success(f"{ok} unlocked · {fail} failed (check the list above).")


# ── Worker that supports per-file output dir ──────────────────────────────

class _MultiUnlockWorker(QThread):
    progress = pyqtSignal(int, str, bool)
    finished = pyqtSignal(int, int)

    def __init__(self, paths: list[str], password: str, out_dir: str):
        super().__init__()
        self._paths = paths
        self._password = password
        self._out_dir = out_dir  # "" means same dir as source

    def run(self):
        ok = fail = 0
        for i, src in enumerate(self._paths):
            p = Path(src)
            folder = self._out_dir if self._out_dir else str(p.parent)
            dst = os.path.join(folder, f"{p.stem}_unlocked.pdf")
            try:
                pdf_ops.remove_password(src, self._password, dst)
                self.progress.emit(i, p.name, True)
                ok += 1
            except Exception as exc:
                self.progress.emit(i, f"{p.name}: {exc}", False)
                fail += 1
        self.finished.emit(ok, fail)
