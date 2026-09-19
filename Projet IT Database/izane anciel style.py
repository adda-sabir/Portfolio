"""
style_pro_blue.py - Fond Bleu-Gris Professionnel
"""
STYLESHEET = """
QMainWindow, QWidget { 
    background-color: #2c313c; /* Gris bleu plus clair et pro */
    color: #f1f5f9; 
    font-family: 'Segoe UI'; 
    font-size: 22px; 
}
QTabWidget::pane { border: 1px solid #3e4451; background-color: #2c313c; }
QTabBar::tab { 
    background-color: #21252b; 
    color: #9da5b4; 
    padding: 12px 28px; 
    font-weight: bold; 
    border-top-left-radius: 4px; border-top-right-radius: 4px;
}
QTabBar::tab:selected { 
    background-color: #3e4451; 
    color: #00a3ff; 
    border-bottom: 3px solid #00a3ff; 
}
QGroupBox { 
    border: 1px solid #3e4451; 
    border-radius: 8px; 
    margin-top: 16px; 
    padding: 14px; 
    color: #00a3ff; 
}
QLineEdit, QComboBox { 
    background-color: #21252b; 
    border: 1px solid #4b5262; 
    border-radius: 4px; 
    color: #abb2bf;
}
QLabel { color: #abb2bf; }
"""