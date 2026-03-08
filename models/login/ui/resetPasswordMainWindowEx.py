import sys, os, csv
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from models.login.ui.resetPasswordMainWindow import Ui_MainWindow


class ResetPasswordWindow(QMainWindow):
    def __init__(self, email):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Lưu lại email được truyền từ trang Verify
        self.user_email = email

        # Tìm đường dẫn file dữ liệu
        self.file_path = self.find_csv_path()

        # Kết nối sự kiện nút Reset và nút Back
        self.ui.pushButtonResetAction.clicked.connect(self.handle_reset_password)

        if hasattr(self.ui, 'pushButtonBack'):
            self.ui.pushButtonBack.clicked.connect(self.handle_back_to_login)

    def find_csv_path(self):
        """Tìm file customerin4.csv"""
        paths_to_check = [
            Path(__file__).parent / "customerin4.csv",
            Path(__file__).parent.parent / "datasets" / "customerin4.csv",
            Path("D:/FINALPROJECT/datasets/customerin4.csv")
        ]
        for p in paths_to_check:
            if p.exists():
                return p
        return Path("customerin4.csv")

    def handle_reset_password(self):
        """Bước 3: Xử lý cập nhật mật khẩu mới vào file CSV"""
        new_pass = self.ui.lineEditNewPass.text().strip()
        confirm_pass = self.ui.lineEditConfirmNewPass.text().strip()

        # 1. Kiểm tra tính hợp lệ
        if not new_pass or not confirm_pass:
            return QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ mật khẩu mới!")

        if new_pass != confirm_pass:
            return QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")

        if len(new_pass) < 6:
            return QMessageBox.warning(self, "Lỗi", "Mật khẩu mới phải từ 6 ký tự trở lên!")

        # 2. Đọc toàn bộ dữ liệu và cập nhật
        try:
            updated_data = []
            found = False

            if not self.file_path.exists():
                return QMessageBox.critical(self, "Lỗi", "Không tìm thấy file dữ liệu hệ thống!")

            with open(self.file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    # File của bạn: cột 2 là Email, cột 6 là Mật khẩu
                    if len(row) > 6 and row[2].strip().lower() == self.user_email.lower():
                        row[6] = new_pass  # Cập nhật mật khẩu mới vào cột thứ 7
                        found = True
                    updated_data.append(row)

            if found:
                # 3. Ghi lại toàn bộ dữ liệu vào file CSV
                with open(self.file_path, mode='w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerows(updated_data)

                # Bước 4: Hoàn tất và quay về Login
                QMessageBox.information(self, "Thành công", "Đổi mật khẩu thành công! Vui lòng đăng nhập lại.")
                self.handle_back_to_login()
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy tài khoản để cập nhật!")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi hệ thống khi cập nhật dữ liệu: {e}")

    def handle_back_to_login(self):
        """Quay lại màn hình Đăng nhập"""
        try:
            from loginMainWindowEx import LoginMainWindowEx
            self.login = LoginMainWindowEx()
            self.login.show()
            self.close()
        except Exception as e:
            print(f"Lỗi khi quay về Login: {e}")
            self.close()


# Khởi chạy độc lập để test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResetPasswordWindow("test@gmail.com")
    window.show()
    sys.exit(app.exec())