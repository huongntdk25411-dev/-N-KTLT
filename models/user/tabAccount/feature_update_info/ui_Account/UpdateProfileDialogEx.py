import os
import csv
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDialog, QMessageBox

from models.user.tabAccount.feature_update_info.ui_Account.UpdateProfileDialog import Ui_Dialog


class UpdateProfileDialogEx(QDialog, Ui_Dialog):

    def __init__(self, user_email=None):
        super().__init__()
        self.setupUi(self)

        # ------------------------------------------------
        # xác định đường dẫn PROJECT ROOT
        # ------------------------------------------------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../../../.."))

        self.filepath = os.path.join(PROJECT_ROOT, "datasets", "customerin4.csv")

        print("CSV PATH:", self.filepath)

        # email user đang login
        self.user_email = user_email

        self.all_users = []
        self.csv_headers = []
        self.current_user_index = -1

        # load dữ liệu
        self.load_profile()

        self.setupSignalAndSlot()

    # ------------------------------------------------
    def setupSignalAndSlot(self):
        self.pushButtonCancel.clicked.connect(self.processCancel)
        self.pushButtonConfirm.clicked.connect(self.processConfirm)

    # ------------------------------------------------
    # load dữ liệu từ CSV
    # ------------------------------------------------
    def load_profile(self):

        if not os.path.exists(self.filepath):
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy file customerin4.csv")
            return

        with open(self.filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            self.csv_headers = reader.fieldnames
            self.all_users = list(reader)

        # tìm user theo email
        for i, user in enumerate(self.all_users):

            if user.get("Email", "").strip().lower() == self.user_email.strip().lower():
                self.current_user_index = i
                break

        if self.current_user_index == -1:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy người dùng")
            return

        user_data = self.all_users[self.current_user_index]

        # --------------------------
        # HIỂN THỊ DỮ LIỆU
        # --------------------------

        self.lineEditName.setText(user_data.get("Họ và tên", ""))

        self.lineEditEmail.setText(user_data.get("Email", ""))
        self.lineEditEmail.setEnabled(False)

        self.lineEditPhone.setText(user_data.get("Số điện thoại", ""))

        # xử lý ngày sinh
        dob_str = user_data.get("Ngày sinh", "") or user_data.get("Ngày tháng năm sinh", "")

        dob = QDate.fromString(dob_str, "dd/MM/yyyy")

        if dob.isValid():
            self.dateEditDOB.setDate(dob)
        else:
            self.dateEditDOB.setDate(QDate(2000, 1, 1))

        gender = user_data.get("Giới tính", "")

        if gender == "Nam":
            self.radioButtonMale.setChecked(True)

        elif gender == "Nữ":
            self.radioButtonFemale.setChecked(True)

    # ------------------------------------------------
    # cập nhật dữ liệu
    # ------------------------------------------------
    def processConfirm(self):

        if self.current_user_index == -1:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy người dùng")
            return

        name = self.lineEditName.text().strip()
        email = self.lineEditEmail.text().strip()
        phone = self.lineEditPhone.text().strip()

        dob = self.dateEditDOB.date().toString("dd/MM/yyyy")

        if self.radioButtonMale.isChecked():
            gender = "Nam"

        elif self.radioButtonFemale.isChecked():
            gender = "Nữ"

        else:
            gender = "Khác"

        # cập nhật dữ liệu
        self.all_users[self.current_user_index]["Họ và tên"] = name
        self.all_users[self.current_user_index]["Email"] = email
        self.all_users[self.current_user_index]["Số điện thoại"] = phone
        self.all_users[self.current_user_index]["Ngày sinh"] = dob
        self.all_users[self.current_user_index]["Giới tính"] = gender

        expected_columns = [
            "Họ và tên",
            "Email",
            "Số điện thoại",
            "Ngày sinh",
            "Giới tính"
        ]

        if not self.csv_headers:
            self.csv_headers = expected_columns.copy()

        else:
            for col in expected_columns:
                if col not in self.csv_headers:
                    self.csv_headers.append(col)

        try:

            with open(self.filepath, "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_headers)

                writer.writeheader()
                writer.writerows(self.all_users)

            QMessageBox.information(self, "Thông báo", "Cập nhật thành công")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    # ------------------------------------------------
    # hủy
    # ------------------------------------------------
    def processCancel(self):

        reply = QMessageBox.question(
            self,
            "Xác nhận hủy",
            "Bạn có chắc chắn muốn hủy bỏ các thay đổi không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.reject()