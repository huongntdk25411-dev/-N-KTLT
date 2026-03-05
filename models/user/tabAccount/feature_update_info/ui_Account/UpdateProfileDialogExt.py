import csv
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QMessageBox

from models.user.tabAccount.feature_update_info.ui_Account.UpdateProfileDialog import Ui_Dialog


class UpdateProfileDialogExt(QDialog,Ui_Dialog):
    def __init__(self,user_email=None):
        super().__init__()
        self.setupUi(self)
        self.filepath="D:/-N-KTLT/datasets/customerin4.csv"
        self.user_email=user_email
        self.all_users=[]
        self.csv_headers=[]
        #mặc định index là -1 (chưa tìm thấy)
        self.current_user_index=-1
        self.load_profile()
        self.setupSignalAndSlot()
    def setupSignalAndSlot(self):
        self.pushButtonCancel.clicked.connect(self.processCancel)
        self.pushButtonConfirm.clicked.connect(self.processConfirm)
    # đọc dữ liệu từ file csv
    def load_profile(self):
        with open(self.filepath,"r",encoding="utf-8-sig") as f:
            reader=csv.DictReader(f)
            self.csv_headers=reader.fieldnames
            self.all_users=list(reader)
        # dò tìm index của user dựa vào email
        for i,user in enumerate(self.all_users):
            if user.get("Email") == self.user_email:
                self.current_user_index=i
                break
        # nếu tìm thấy user
        if self.current_user_index!=-1:
            user_data=self.all_users[self.current_user_index]
            self.lineEditName.setText(user_data.get("Họ và tên",""))
            # Gán email và KHÓA LẠI KHÔNG CHO SỬA EMAIL (để tránh lỗi mất khóa chính)
            self.lineEditEmail.setText(user_data.get("Email", ""))
            self.lineEditEmail.setEnabled(False)
            self.lineEditPhone.setText(user_data.get("Số điện thoại",""))

            dob_str=user_data.get("Ngày sinh","")
            dob=QDate.fromString(dob_str,"dd/MM/yyyy")
            if dob.isValid():
                self.dateEditDOB.setDate(dob)
            else:
                #nếu ko có ngày sinh/ lỗi format -> set về mặc định là 1/1/1999
                self.dateEditDOB.setDate(QDate(1999,1,1))

            gender=user_data.get("Giới tính","")
            if gender == "Nam":
                self.radioButtonMale.setChecked(True)
            elif gender == "Nữ":
                self.radioButtonFemale.setChecked(True)

    def processConfirm(self):
        #lấy dữ liệu từ giao diện
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

        #cập nhật thông tin vào đúng index đã tìm thấy
        self.all_users[self.current_user_index]["Họ và tên"]=name
        self.all_users[self.current_user_index]["Email"]=email
        self.all_users[self.current_user_index]["Số điện thoại"] = phone
        self.all_users[self.current_user_index]["Ngày sinh"] = dob
        self.all_users[self.current_user_index]["Giới tính"] = gender

        # Tự động bổ sung các cột mới vào header nếu file CSV cũ chưa có
        expected_columns = ["Họ và tên", "Email", "Số điện thoại", "Ngày sinh", "Giới tính"]
        if not self.csv_headers:
            self.csv_headers=expected_columns.copy()
        else:
            for col in expected_columns:
                if col not in self.csv_headers:
                    self.csv_headers.append(col)

        # Ghi toàn bộ dữ liệu lại vào file CSV
        with open(self.filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.csv_headers)
            writer.writeheader()
            writer.writerows(self.all_users)

        QMessageBox.information(self, "Thông báo", "Cập nhật thành công")
        # close dialog and back to accepted
        self.accept()

    def processCancel(self):
        reply=QMessageBox.question(
            self,
            "Xác nhận hủy",
            "Bạn có chắc chắn muốn hủy bỏ các thay đổi không?",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
        )
        if reply==QMessageBox.StandardButton.Yes:
            self.reject()