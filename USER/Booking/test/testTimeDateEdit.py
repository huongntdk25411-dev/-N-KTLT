from PyQt6.QtWidgets import QApplication, QMainWindow

from Final.timeDateEdit_Customers.MainWindowEx import MainWindowEx

app = QApplication([])

mainWindow = QMainWindow()
gui = MainWindowEx()
gui.setupUi(mainWindow)
gui.show()

app.exec()
