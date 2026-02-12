from PyQt6.QtWidgets import QApplication

from feature_update_profile.ui.UpdateProfileDialogExt import UpdateProfileDialogExt

app=QApplication([])
w=UpdateProfileDialogExt()

w.show()
app.exec()