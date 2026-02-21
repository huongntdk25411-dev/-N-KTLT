import sys
import os
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from registerMainWindow import Ui_MainWindow


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # CỐ ĐỊNH MÀU CHỮ ĐEN CHO CÁC Ô NHẬP LIỆU
        inputs = [self.ui.lineEditName, self.ui.lineEditEmail, self.ui.lineEditUser, self.ui.lineEditPass]
        for item in inputs:
            item.setStyleSheet(item.styleSheet() + "color: black;")

        # Thiết lập đường dẫn lưu trữ dữ liệu
        self.dataset_dir = "dataset"
        self.file_path = os.path.join(self.dataset_dir, "customerin4.csv")

        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)

        self.ui.pushButtonRegister.clicked.connect(self.handle_register)
        self.ui.pushButtonBack.clicked.connect(self.handle_back)

    # ... (Các phần code handle_register và handle_back giữ nguyên như cũ)
    def handle_register(self):
        fullname = self.ui.lineEditName.text().strip()
        email = self.ui.lineEditEmail.text().strip()
        username = self.ui.lineEditUser.text().strip()
        password = self.ui.lineEditPass.text().strip()
        gender = "Nam" if self.ui.radMale.isChecked() else "Nữ"

        if not all([fullname, email, username, password]):
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng điền đầy đủ các thông tin có dấu *!")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Lỗi mật khẩu", "Mật khẩu quá ngắn! Vui lòng nhập ít nhất 6 ký tự.")
            return

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, mode='r', encoding='utf-8-sig') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row.get('Email') == email:
                            QMessageBox.warning(self, "Lỗi đăng ký", f"Email '{email}' đã được đăng ký!")
                            return
                        if row.get('Tên đăng nhập') == username:
                            QMessageBox.warning(self, "Lỗi đăng ký", f"Tên đăng nhập '{username}' đã tồn tại!")
                            return
            except Exception as e:
                print(f"Lỗi khi đọc file kiểm tra: {e}")

        try:
            file_exists = os.path.isfile(self.file_path)
            with open(self.file_path, mode='a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Họ và tên", "Email", "Tên đăng nhập", "Mật khẩu", "Giới tính"])
                writer.writerow([fullname, email, username, password, gender])

            QMessageBox.information(self, "Thành công", f"Tài khoản '{username}' đã được tạo thành công!")
            self.handle_back()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Không thể lưu dữ liệu: {str(e)}")

    def handle_back(self):
        try:
            from loginMainWindowEx import LoginMainWindowEx
            self.login_win = LoginMainWindowEx()
            self.login_win.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi chuyển hướng", f"Không thể quay lại màn hình đăng nhập: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())