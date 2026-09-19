from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from database import init_db
from gui import FenetrePrincipale
from style import STYLESHEET
import sys

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    app.setFont(QFont("Segoe UI", 10))
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec())