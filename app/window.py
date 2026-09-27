"""
Main window — sidebar navigation + stacked tool pages.
Clean, minimal layout with smooth tool switching.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QStackedWidget, QPushButton, QLabel, QSizePolicy, QApplication,
)

from app.theme import SIDEBAR_WIDTH
from app.tools.password_tool import PasswordTool
from app.tools.merge_tool import MergeTool
from app.tools.split_tool import SplitTool
from app.tools.rotate_tool import RotateTool
from app.tools.compress_tool import CompressTool
from app.tools.watermark_tool import WatermarkTool
from app.tools.pdf_to_img import PdfToImgTool
from app.tools.img_to_pdf import ImgToPdfTool
from app.tools.reorder_tool import ReorderTool
from app.tools.metadata_tool import MetadataTool


# (icon, label, ToolClass)
TOOLS = [
    ("🔓", "Remove Password", PasswordTool),
    ("📑", "Merge PDFs", MergeTool),
    ("✂️", "Split PDF", SplitTool),
    ("🔄", "Rotate Pages", RotateTool),
    ("📦", "Compress", CompressTool),
    ("💧", "Watermark", WatermarkTool),
    ("🖼️", "PDF → Images", PdfToImgTool),
    ("📷", "Images → PDF", ImgToPdfTool),
    ("↕️", "Reorder Pages", ReorderTool),
    ("🏷️", "Edit Metadata", MetadataTool),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scribe")
        self.setMinimumSize(960, 640)
        self.resize(1080, 720)

        # ── Central widget ──
        central = QWidget()
        central.setObjectName("central_widget")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # App branding
        title = QLabel("Scribe")
        title.setObjectName("sidebar_title")
        sidebar_layout.addWidget(title)

        subtitle = QLabel("PDF Workbench")
        subtitle.setObjectName("sidebar_subtitle")
        sidebar_layout.addWidget(subtitle)

        # Separator
        sep = QFrame()
        sep.setProperty("class", "separator")
        sep.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(8)

        # Navigation buttons
        self._nav_buttons: list[QPushButton] = []
        self._stack = QStackedWidget()

        for i, (icon, label, ToolClass) in enumerate(TOOLS):
            # Create nav button
            btn = QPushButton(f"  {icon}   {label}")
            btn.setProperty("class", "nav_btn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=i: self._switch_tool(idx))
            sidebar_layout.addWidget(btn)
            self._nav_buttons.append(btn)

            # Create tool page
            tool_page = ToolClass()
            self._stack.addWidget(tool_page)

        sidebar_layout.addStretch()

        # Version label at bottom
        ver = QLabel("v1.0.0")
        ver.setObjectName("sidebar_subtitle")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(ver)
        sidebar_layout.addSpacing(12)

        root.addWidget(sidebar)
        root.addWidget(self._stack, 1)

        # Select first tool
        self._current = -1
        self._switch_tool(0)

    @staticmethod
    def _refresh_style(w: QWidget):
        style = w.style()
        if style is not None:
            style.unpolish(w)
            style.polish(w)

    def _switch_tool(self, idx: int):
        if idx == self._current:
            return
        # Deactivate old
        if 0 <= self._current < len(self._nav_buttons):
            old_btn = self._nav_buttons[self._current]
            old_btn.setProperty("active", "false")
            self._refresh_style(old_btn)

        # Activate new
        self._current = idx
        self._stack.setCurrentIndex(idx)
        btn = self._nav_buttons[idx]
        btn.setProperty("active", "true")
        self._refresh_style(btn)
