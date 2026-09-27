"""
Dark minimal theme — color palette, fonts, and QSS stylesheet.
Inspired by GitHub Dark with a single blue accent.
"""

# ── Color Palette ────────────────────────────────────────────────────────

BG_DARKEST   = "#08090d"   # Sidebar background
BG_DARK      = "#0d1117"   # Main background
BG_CARD      = "#151b23"   # Cards / panels
BG_INPUT     = "#1c2128"   # Input fields
BG_HOVER     = "#1c2128"   # Sidebar hover
BG_ACTIVE    = "#1a2233"   # Sidebar active item

BORDER       = "#2a3040"   # Subtle borders
BORDER_LIGHT = "#3d444d"   # Slightly more visible borders

TEXT         = "#e6edf3"   # Primary text
TEXT_DIM     = "#7d8590"   # Secondary / muted text
TEXT_DARK    = "#484f58"   # Disabled / very muted

ACCENT       = "#58a6ff"   # Primary accent
ACCENT_HOVER = "#79c0ff"   # Accent on hover
ACCENT_BG    = "#152238"   # Accent tinted background

SUCCESS      = "#3fb950"
ERROR        = "#f85149"
WARNING      = "#d29922"

# ── Font ─────────────────────────────────────────────────────────────────

FONT_FAMILY  = "Segoe UI, Inter, -apple-system, sans-serif"
FONT_SIZE    = "13px"
FONT_SIZE_SM = "11px"
FONT_SIZE_LG = "15px"
FONT_SIZE_XL = "22px"

# ── Dimensions ───────────────────────────────────────────────────────────

SIDEBAR_WIDTH   = 220
RADIUS          = "8px"
RADIUS_SM       = "6px"
RADIUS_LG       = "12px"

# ── QSS Stylesheet ──────────────────────────────────────────────────────

STYLESHEET = f"""
/* ── Global ────────────────────────────────── */
* {{
    font-family: {FONT_FAMILY};
    font-size: {FONT_SIZE};
    color: {TEXT};
    outline: none;
}}

QMainWindow {{
    background: {BG_DARK};
}}

/* ── Sidebar ───────────────────────────────── */
#sidebar {{
    background: {BG_DARKEST};
    border-right: 1px solid {BORDER};
    min-width: {SIDEBAR_WIDTH}px;
    max-width: {SIDEBAR_WIDTH}px;
}}

#sidebar_title {{
    font-size: {FONT_SIZE_LG};
    font-weight: 700;
    color: {TEXT};
    padding: 24px 20px 8px 20px;
}}

#sidebar_subtitle {{
    font-size: {FONT_SIZE_SM};
    color: {TEXT_DIM};
    padding: 0 20px 16px 20px;
}}

/* Sidebar buttons */
QPushButton[class="nav_btn"] {{
    background: transparent;
    border: none;
    border-radius: {RADIUS_SM};
    text-align: left;
    padding: 10px 16px;
    margin: 1px 8px;
    font-size: {FONT_SIZE};
    color: {TEXT_DIM};
}}

QPushButton[class="nav_btn"]:hover {{
    background: {BG_HOVER};
    color: {TEXT};
}}

QPushButton[class="nav_btn"][active="true"] {{
    background: {ACCENT_BG};
    color: {ACCENT};
    font-weight: 600;
}}

/* ── Scroll area ───────────────────────────── */
QScrollArea {{
    background: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {BORDER_LIGHT};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}

/* ── Tool pages ────────────────────────────── */
#tool_page {{
    background: {BG_DARK};
}}

#tool_title {{
    font-size: {FONT_SIZE_XL};
    font-weight: 700;
    color: {TEXT};
    padding: 0;
    margin: 0;
}}

#tool_desc {{
    font-size: {FONT_SIZE};
    color: {TEXT_DIM};
    padding: 0;
    margin: 0;
}}

/* ── Cards ─────────────────────────────────── */
QFrame[class="card"] {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
}}

/* ── Drop zone ─────────────────────────────── */
#drop_zone {{
    background: {BG_CARD};
    border: 2px dashed {BORDER_LIGHT};
    border-radius: {RADIUS_LG};
    min-height: 140px;
}}

#drop_zone[dragover="true"] {{
    border-color: {ACCENT};
    background: {ACCENT_BG};
}}

#drop_zone_icon {{
    font-size: 28px;
    color: {TEXT_DIM};
}}

#drop_zone_text {{
    font-size: {FONT_SIZE};
    color: {TEXT_DIM};
}}

#drop_zone_hint {{
    font-size: {FONT_SIZE_SM};
    color: {TEXT_DARK};
}}

/* ── Buttons ───────────────────────────────── */
QPushButton[class="primary"] {{
    background: {ACCENT};
    color: #ffffff;
    border: none;
    border-radius: {RADIUS_SM};
    padding: 10px 28px;
    font-weight: 600;
    font-size: {FONT_SIZE};
}}

QPushButton[class="primary"]:hover {{
    background: {ACCENT_HOVER};
}}

QPushButton[class="primary"]:disabled {{
    background: {BORDER};
    color: {TEXT_DARK};
}}

QPushButton[class="secondary"] {{
    background: {BG_INPUT};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 10px 20px;
    font-size: {FONT_SIZE};
}}

QPushButton[class="secondary"]:hover {{
    border-color: {BORDER_LIGHT};
    background: {BG_HOVER};
}}

QPushButton[class="danger"] {{
    background: transparent;
    color: {ERROR};
    border: 1px solid {ERROR};
    border-radius: {RADIUS_SM};
    padding: 8px 16px;
    font-size: {FONT_SIZE};
}}

QPushButton[class="danger"]:hover {{
    background: #f8514922;
}}

QPushButton[class="icon_btn"] {{
    background: transparent;
    border: none;
    padding: 6px;
    border-radius: {RADIUS_SM};
    font-size: 16px;
    color: {TEXT_DIM};
}}

QPushButton[class="icon_btn"]:hover {{
    background: {BG_HOVER};
    color: {TEXT};
}}

/* ── Inputs ────────────────────────────────── */
QLineEdit, QSpinBox, QDoubleSpinBox {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 9px 12px;
    color: {TEXT};
    selection-background-color: {ACCENT_BG};
}}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {ACCENT};
}}

QLineEdit:disabled {{
    background: {BG_DARKEST};
    color: {TEXT_DARK};
}}

/* ── Combo box ─────────────────────────────── */
QComboBox {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 9px 12px;
    color: {TEXT};
    min-width: 100px;
}}

QComboBox:hover {{
    border-color: {BORDER_LIGHT};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXT_DIM};
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    selection-background-color: {ACCENT_BG};
    selection-color: {ACCENT};
    padding: 4px;
}}

/* ── Labels ────────────────────────────────── */
QLabel[class="field_label"] {{
    font-size: {FONT_SIZE_SM};
    color: {TEXT_DIM};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 0;
    margin: 0;
}}

QLabel[class="status_success"] {{
    color: {SUCCESS};
    font-size: {FONT_SIZE};
}}

QLabel[class="status_error"] {{
    color: {ERROR};
    font-size: {FONT_SIZE};
}}

QLabel[class="file_label"] {{
    color: {TEXT};
    font-size: {FONT_SIZE};
    padding: 8px 12px;
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
}}

/* ── Slider ────────────────────────────────── */
QSlider::groove:horizontal {{
    background: {BORDER};
    height: 4px;
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT};
    border-radius: 2px;
}}

/* ── Progress bar ──────────────────────────── */
QProgressBar {{
    background: {BG_INPUT};
    border: none;
    border-radius: 4px;
    height: 6px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: {ACCENT};
    border-radius: 4px;
}}

/* ── Separator ─────────────────────────────── */
QFrame[class="separator"] {{
    background: {BORDER};
    max-height: 1px;
    min-height: 1px;
}}

/* ── Tooltips ──────────────────────────────── */
QToolTip {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    color: {TEXT};
    padding: 6px 10px;
    font-size: {FONT_SIZE_SM};
}}

/* ── List widget (file list, page list) ────── */
QListWidget {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_SM};
    padding: 4px;
    outline: none;
}}

QListWidget::item {{
    padding: 8px 12px;
    border-radius: {RADIUS_SM};
    margin: 1px 0;
}}

QListWidget::item:selected {{
    background: {ACCENT_BG};
    color: {ACCENT};
}}

QListWidget::item:hover:!selected {{
    background: {BG_HOVER};
}}
"""
