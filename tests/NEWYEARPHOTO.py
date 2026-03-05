from PyQt6.QtWidgets import QApplication

from models.login.ui.loginMainWindowEx import LoginMainWindowEx

app = QApplication([])

gui = LoginMainWindowEx()
gui.show()

app.exec()