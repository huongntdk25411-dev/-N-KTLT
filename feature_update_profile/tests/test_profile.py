from PyQt6.QtWidgets import QApplication, QMainWindow

from feature_update_profile.ui.ProfileWindowExt import ProfileWindowExt

app=QApplication([])
w=ProfileWindowExt()

w.show()
app.exec()