from PyQt6.QtWidgets import QApplication

from models.user.tabAccount.feature_update_info.ui_Account.UpdateProfileDialogEx import UpdateProfileDialogEx

app=QApplication([])
w=UpdateProfileDialogEx()

w.show()
app.exec()