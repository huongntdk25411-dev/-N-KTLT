import json
import os

from PyQt6.QtWidgets import QMainWindow

from feature_update_profile.ui.ProfileWindow import Ui_MainWindow
from feature_update_profile.ui.UpdateProfileDialogExt import UpdateProfileDialogExt


class ProfileWindowExt(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_path="../datasets/user_profile.json"

        #load initial data
        self.load_profile()

        self.pushButtonUpdate.clicked.connect(self.open_update_dialog)

    #read json file và show on ui
    def load_profile(self):
        if not os.path.exists(self.file_path):
            return {}

        with open(self.file_path, "r", encoding="utf-8") as f:
            data=json.load(f)

        self.labelUsername.setText(data.get("name",""))
        self.labelName.setText(data.get("name",""))
        self.labelEmail.setText(data.get("email",""))
        self.labelPhone.setText(data.get("phone",""))
        self.labelDOB.setText(data.get("dob",""))
        self.labelGender.setText(data.get("gender",""))

    #open dialog
    def open_update_dialog(self):
        dlg=UpdateProfileDialogExt()
        result=dlg.exec()
        if result: #if push Confirm Button (accepted)
            #read file after update
            self.profile_data=self.load_profile()