import json
import os

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QMessageBox

from feature_update_profile.ui.UpdateProfileDialog import Ui_Dialog


class UpdateProfileDialogExt(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_path="../datasets/user_profile.json"
        #load data on form
        self.load_profile()
        #connect signal
        self.pushButtonConfirm.clicked.connect(self.process_confirm)
        self.pushButtonCancel.clicked.connect(self.process_cancel)


    #read json file
    def load_profile(self):
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.lineEditName.setText(data.get("name",""))
        self.lineEditEmail.setText(data.get("email",""))
        self.lineEditPhone.setText(data.get("phone",""))
        dob=QDate.fromString(data.get("dob",""),"dd/MM/yyyy")
        if dob.isValid():
            self.dateEditDOB.setDate(dob)

        gender=data.get("gender","")
        if gender=="Nam":
            self.radioButtonMale.setChecked(True)
        elif gender=="Nữ":
            self.radioButtonFemale.setChecked(True)

    def process_confirm(self):
        name=self.lineEditName.text().strip()
        email=self.lineEditEmail.text().strip()
        phone=self.lineEditPhone.text().strip()
        dob=self.dateEditDOB.date().toString("dd/MM/yyyy")
        if self.radioButtonMale.isChecked():
            gender="Nam"
        elif self.radioButtonFemale.isChecked():
            gender="Nữ"
        else:
            gender="Khác"

        #validation
        if name=="" or email=="" or phone=="":
            QMessageBox.warning(self,"Lỗi","Vui lòng nhập đầy đủ thông tin")
            return
        #update dict
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "dob": dob,
            "gender": gender
        }

        #note to JSON file
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)

        QMessageBox.information(self,"Thông báo","Cập nhật thành công")

        #close dialog and back to accepted
        self.accept()

    def process_cancel(self):
        reply=QMessageBox.question(
            self,
            "Xác nhận hủy",
            "Bạn có chắc chắn muốn hủy bỏ các thay đổi không?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
        )
        if reply==QMessageBox.StandardButton.Yes:
            self.reject()