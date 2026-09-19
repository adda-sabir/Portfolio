"""
style_pro_blue.py - Fond Bleu-Gris Professionnel (v2 - couverture complète)
"""
STYLESHEET = """

/* ───── BASE ───── */
QMainWindow, QWidget {
    background-color: #2c313c;
    color: #f1f5f9;
    font-family: 'Segoe UI';
    font-size: 22px;
}

/* ───── ONGLETS ───── */
QTabWidget::pane {
    border: 1px solid #3e4451;
    background-color: #2c313c;
}
QTabBar::tab {
    background-color: #21252b;
    color: #9da5b4;
    padding: 12px 28px;
    font-weight: bold;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
QTabBar::tab:selected {
    background-color: #3e4451;
    color: #00a3ff;
    border-bottom: 3px solid #00a3ff;
}
QTabBar::tab:hover:!selected {
    background-color: #2c313c;
    color: #d0d7e3;
}

/* ───── GROUPBOX ───── */
QGroupBox {
    border: 1px solid #3e4451;
    border-radius: 8px;
    margin-top: 16px;
    padding: 14px;
    color: #00a3ff;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #00a3ff;
}

/* ───── CHAMPS & LABELS ───── */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #21252b;
    border: 1px solid #4b5262;
    border-radius: 4px;
    color: #abb2bf;
    padding: 4px 8px;
    selection-background-color: #00a3ff;
    selection-color: #ffffff;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #00a3ff;
}
QLabel {
    color: #abb2bf;
    background-color: transparent;
}

/* ───── COMBOBOX ───── */
QComboBox {
    background-color: #21252b;
    border: 1px solid #4b5262;
    border-radius: 4px;
    color: #abb2bf;
    padding: 4px 8px;
}
QComboBox:focus {
    border: 1px solid #00a3ff;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #9da5b4;
    width: 0;
    height: 0;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #21252b;
    border: 1px solid #4b5262;
    color: #abb2bf;
    selection-background-color: #00a3ff;
    selection-color: #ffffff;
    outline: none;
}

/* ───── BOUTONS ───── */
QPushButton {
    background-color: #3e4451;
    color: #abb2bf;
    border: 1px solid #4b5262;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #4b5262;
    color: #f1f5f9;
    border: 1px solid #00a3ff;
}
QPushButton:pressed {
    background-color: #00a3ff;
    color: #ffffff;
}
QPushButton:disabled {
    background-color: #2c313c;
    color: #555d6e;
    border-color: #3e4451;
}

/* ───── TABLEAU ───── */
QTableWidget, QTableView {
    background-color: #21252b;
    alternate-background-color: #272c36;
    color: #abb2bf;
    border: 1px solid #3e4451;
    gridline-color: #3e4451;
    selection-background-color: #00a3ff;
    selection-color: #ffffff;
    border-radius: 4px;
}
QTableWidget::item, QTableView::item {
    padding: 6px 10px;
}
QTableWidget::item:selected, QTableView::item:selected {
    background-color: #1a6fa8;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #2c313c;
    color: #9da5b4;
    border: none;
    border-bottom: 2px solid #00a3ff;
    padding: 6px 10px;
    font-weight: bold;
}
QHeaderView::section:hover {
    background-color: #3e4451;
    color: #f1f5f9;
}
QTableWidget QTableCornerButton::section {
    background-color: #2c313c;
    border: none;
}

/* ───── SCROLLBARS ───── */
QScrollBar:vertical {
    background-color: #21252b;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background-color: #4b5262;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background-color: #00a3ff;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background-color: #21252b;
    height: 10px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background-color: #4b5262;
    border-radius: 5px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #00a3ff;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ───── SPINBOX ───── */
QSpinBox, QDoubleSpinBox {
    background-color: #21252b;
    border: 1px solid #4b5262;
    border-radius: 4px;
    color: #abb2bf;
    padding: 4px 8px;
}
QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid #00a3ff;
}
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background-color: #3e4451;
    border: none;
    width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #00a3ff;
}

/* ───── CHECKBOX & RADIO ───── */
QCheckBox, QRadioButton {
    color: #abb2bf;
    spacing: 8px;
}
QCheckBox::indicator, QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #4b5262;
    border-radius: 3px;
    background-color: #21252b;
}
QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #00a3ff;
    border-color: #00a3ff;
}

/* ───── DIALOG & MESSAGEBOX ───── */
QDialog {
    background-color: #2c313c;
}
QMessageBox {
    background-color: #2c313c;
    color: #f1f5f9;
}

/* ───── MENU ───── */
QMenuBar {
    background-color: #21252b;
    color: #9da5b4;
}
QMenuBar::item:selected {
    background-color: #3e4451;
    color: #f1f5f9;
}
QMenu {
    background-color: #21252b;
    border: 1px solid #3e4451;
    color: #abb2bf;
}
QMenu::item:selected {
    background-color: #00a3ff;
    color: #ffffff;
}

/* ───── STATUSBAR ───── */
QStatusBar {
    background-color: #21252b;
    color: #9da5b4;
    border-top: 1px solid #3e4451;
}

/* ───── TOOLTIP ───── */
QToolTip {
    background-color: #3e4451;
    color: #f1f5f9;
    border: 1px solid #00a3ff;
    padding: 4px 8px;
    border-radius: 4px;
}

"""
