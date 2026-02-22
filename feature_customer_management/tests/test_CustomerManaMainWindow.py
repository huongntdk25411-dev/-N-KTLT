from PyQt6.QtWidgets import QApplication

from feature_customer_management.ui.CustomerManaMainWindowExt import CustomerManaMainWindowExt

app=QApplication([])
w=CustomerManaMainWindowExt()
w.show()
app.exec()