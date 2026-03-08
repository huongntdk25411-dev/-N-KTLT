import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from PyQt6.QtWidgets import QApplication
from models.login.ui.loginMainWindowEx import LoginMainWindowEx

app = QApplication(sys.argv)
window = LoginMainWindowEx()
window.show()
sys.exit(app.exec())
