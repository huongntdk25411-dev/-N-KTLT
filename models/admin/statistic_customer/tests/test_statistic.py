from PyQt6.QtWidgets import QApplication, QMainWindow

from models.admin.statistic_customer.ui.MainWindowEx import MainWindowEx

qApp=QApplication([])
qmainWindow=QMainWindow()
window=MainWindowEx()
window.setupUi(qmainWindow)
window.show()
qApp.exec()