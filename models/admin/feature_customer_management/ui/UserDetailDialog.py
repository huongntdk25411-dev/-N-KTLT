import csv
import os
from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QMessageBox
)


class UserDetailDialog(QDialog):
    def __init__(self, user):
        super().__init__()

        self.user = user
        self.old_email = user.get("Email")

        # đường dẫn tới datasets/customerin4.csv
        self.file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "..", "..", "..",
                "datasets",
                "customerin4.csv"
            )
        )

        self.setWindowTitle("Chỉnh sửa thông tin khách hàng")
        self.resize(400, 350)

        # input
        self.nameEdit = QLineEdit()
        self.emailEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.birthEdit = QLineEdit()
        self.genderEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        # form layout
        form = QFormLayout()
        form.addRow("Họ và tên:", self.nameEdit)
        form.addRow("Email:", self.emailEdit)
        form.addRow("Số điện thoại:", self.phoneEdit)
        form.addRow("Ngày sinh:", self.birthEdit)
        form.addRow("Giới tính:", self.genderEdit)
        form.addRow("Mật khẩu:", self.passwordEdit)

        self.btnSave = QPushButton("Lưu chỉnh sửa")
        self.btnClose = QPushButton("Hủy")

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btnSave)
        layout.addWidget(self.btnClose)
        self.setLayout(layout)

        self.load_user_data()

        self.btnSave.clicked.connect(self.update_user_csv)
        self.btnClose.clicked.connect(self.reject)

    # hiển thị dữ liệu lên form
    def load_user_data(self):
        self.nameEdit.setText(self.user.get("Họ và tên", ""))
        self.emailEdit.setText(self.user.get("Email", ""))
        self.phoneEdit.setText(self.user.get("Số điện thoại", ""))
        self.birthEdit.setText(self.user.get("Ngày sinh", ""))
        self.genderEdit.setText(self.user.get("Giới tính", ""))
        self.passwordEdit.setText(self.user.get("Mật khẩu", ""))

    # cập nhật lại CSV
    def update_user_csv(self):

        if not os.path.exists(self.file_path):
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy file CSV!")
            return

        try:
            rows = []
            updated = False

            with open(self.file_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames

                for row in reader:

                    if row["Email"] == self.old_email:
                        row["Họ và tên"] = self.nameEdit.text()
                        row["Email"] = self.emailEdit.text()
                        row["Số điện thoại"] = self.phoneEdit.text()
                        row["Ngày sinh"] = self.birthEdit.text()
                        row["Giới tính"] = self.genderEdit.text()
                        row["Mật khẩu"] = self.passwordEdit.text()
                        updated = True

                    rows.append(row)

            if updated:

                with open(self.file_path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

                QMessageBox.information(self, "Thành công", "Đã cập nhật dữ liệu!")
                self.accept()

            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy khách hàng!")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))