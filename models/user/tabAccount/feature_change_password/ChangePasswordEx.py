import csv
from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from models.user.tabAccount.feature_change_password.ChangePasswordMainwindow import Ui_MainWindow


class ChangePasswordEx(QMainWindow):
    def __init__(self, user_email):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_email = user_email

        # Ẩn mật khẩu
        self.ui.lineEditOldPass.setEchoMode(self.ui.lineEditOldPass.EchoMode.Password)
        self.ui.lineEditNewPass.setEchoMode(self.ui.lineEditNewPass.EchoMode.Password)
        self.ui.lineEditNewPass_2.setEchoMode(self.ui.lineEditNewPass_2.EchoMode.Password)
        #open-hide pass
        self.setup_password_toggle(self.ui.lineEditNewPass)
        self.setup_password_toggle(self.ui.lineEditOldPass)
        self.setup_password_toggle(self.ui.lineEditNewPass_2)

        # Tìm đường dẫn datasets
        current_path = Path(__file__).resolve()
        PROJECT_ROOT = None
        for parent in current_path.parents:
            if (parent/"datasets").exists():
                PROJECT_ROOT = parent
                break

        self.csv_path = PROJECT_ROOT /"datasets" /"customerin4.csv"

        # Connect
        self.ui.btnConfirm.clicked.connect(self.change_password)
        self.ui.btnCancel.clicked.connect(self.close)

    # change pass
    def change_password(self):
        try:
            old_pass = self.ui.lineEditOldPass.text().strip()
            new_pass = self.ui.lineEditNewPass.text().strip()
            confirm_pass = self.ui.lineEditNewPass_2.text().strip()

            # TH1: Kiểm tra nhập đầy đủ hay chưa
            if not old_pass or not new_pass or not confirm_pass:
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Vui lòng nhập đầy đủ thông tin!"
                )
                return

            rows = []
            updated = False

            with open(self.csv_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames

                for row in reader:
                    email_in_file = (row.get("Email") or "").strip().lower()

                    if email_in_file == self.user_email.strip().lower():

                        stored_pass = (row.get("Mật khẩu") or "").strip()

                        # TH: Kiểm tra mật khẩu cũ
                        if stored_pass != old_pass:
                            QMessageBox.warning(
                                self,
                                "Lỗi",
                                "Mật khẩu cũ không đúng!"
                            )
                            return

                        # TH: Mật khẩu mới trùng mật khẩu cũ
                        if new_pass == stored_pass:
                            QMessageBox.warning(
                                self,
                                "Lỗi",
                                "Mật khẩu mới không được trùng mật khẩu cũ!"
                            )
                            return

                        # Xác nhận không khớp
                        if new_pass != confirm_pass:
                            QMessageBox.warning(
                                self,
                                "Lỗi",
                                "Mật khẩu xác nhận không khớp!"
                            )
                            return

                        # Nếu hợp lệ -> cập nhật
                        row["Mật khẩu"] = new_pass
                        updated = True

                    rows.append(row)

            if not updated:
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Không tìm thấy tài khoản!"
                )
                return

            # Ghi lại file CSV
            with open(self.csv_path, mode="w", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            QMessageBox.information(
                self,
                "Thành công",
                "Đổi mật khẩu thành công!"
            )

            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Crash", str(e))

    def setup_password_toggle(self, line_edit):
        icon_hidden_path="D:/-N-KTLT/images/ic_hide.png"

        # Thêm icon vào góc bên phải của ô nhập liệu (TrailingPosition)
        action = line_edit.addAction(QIcon(icon_hidden_path), QLineEdit.ActionPosition.TrailingPosition)

        # Kết nối sự kiện click vào icon với hàm toggle
        action.triggered.connect(lambda: self.toggle_password_visibility(line_edit, action))

    def toggle_password_visibility(self, line_edit, action):
        icon_open_path = "D:/-N-KTLT/images/ic_open.png"
        icon_hidden_path="D:/-N-KTLT/images/ic_hide.png"

        # Nếu đang ẩn -> Chuyển sang hiện và đổi icon thành mắt mở
        if line_edit.echoMode() == QLineEdit.EchoMode.Password:
            line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            action.setIcon(QIcon(icon_open_path))
        # Nếu đang hiện -> Chuyển sang ẩn và đổi icon thành mắt nhắm
        else:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            action.setIcon(QIcon(icon_hidden_path))