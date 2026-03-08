import csv
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from models.user.tabAccount.feature_change_password.ChangePasswordMainwindow import Ui_MainWindow


class ChangePasswordEx(QMainWindow):
    def __init__(self, user_email):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_email = user_email

        # Ẩn mật khẩu
        self.ui.lineEditOldPass.setEchoMode(
            self.ui.lineEditOldPass.EchoMode.Password
        )
        self.ui.lineEditNewPass.setEchoMode(
            self.ui.lineEditNewPass.EchoMode.Password
        )
        self.ui.lineEditNewPass_2.setEchoMode(
            self.ui.lineEditNewPass_2.EchoMode.Password
        )

        # Tìm đường dẫn datasets
        current_path = Path(__file__).resolve()
        PROJECT_ROOT = None
        for parent in current_path.parents:
            if (parent / "datasets").exists():
                PROJECT_ROOT = parent
                break

        self.csv_path = PROJECT_ROOT / "datasets" / "customerin4.csv"

        # Connect
        self.ui.btnConfirm.clicked.connect(self.change_password)
        self.ui.btnCancel.clicked.connect(self.close)

    # ==================================================
    # HÀM ĐỔI MẬT KHẨU
    # ==================================================
    def change_password(self):
        try:
            old_pass = self.ui.lineEditOldPass.text().strip()
            new_pass = self.ui.lineEditNewPass.text().strip()
            confirm_pass = self.ui.lineEditNewPass_2.text().strip()

            # 1️⃣ Kiểm tra nhập đầy đủ
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

                        # 2️⃣ Kiểm tra mật khẩu cũ
                        if stored_pass != old_pass:
                            QMessageBox.warning(
                                self,
                                "Lỗi",
                                "Mật khẩu cũ không đúng!"
                            )
                            return

                        # 3️⃣ Mật khẩu mới trùng mật khẩu cũ
                        if new_pass == stored_pass:
                            QMessageBox.warning(
                                self,
                                "Lỗi",
                                "Mật khẩu mới không được trùng mật khẩu cũ!"
                            )
                            return

                        # 4️⃣ Xác nhận không khớp
                        if new_pass != confirm_pass:
                            QMessageBox.warning(
                                self,
                                "Lỗi",
                                "Mật khẩu xác nhận không khớp!"
                            )
                            return

                        # Nếu hợp lệ → cập nhật
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