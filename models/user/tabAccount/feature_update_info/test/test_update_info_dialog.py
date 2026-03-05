from PyQt6.QtWidgets import QApplication

from models.user.tabAccount.feature_update_info.ui_Account.UpdateProfileDialogExt import UpdateProfileDialogExt

app=QApplication([])
w=UpdateProfileDialogExt()

w.show()
app.exec()