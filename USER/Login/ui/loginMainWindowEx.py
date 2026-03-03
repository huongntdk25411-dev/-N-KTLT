import sys
import os
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from loginMainWindow import Ui_MainWindow

class LoginMainWindowEx(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # CỐ ĐỊNH MÀU CHỮ ĐEN CHO CÁC Ô NHẬP LIỆU (Tránh lỗi Dark Mode)
        self.ui.lineEditEmail.setStyleSheet(self.ui.lineEditEmail.styleSheet() + "color: black;")
        self.ui.lineEditPass.setStyleSheet(self.ui.lineEditPass.styleSheet() + "color: black;")

        # Đường dẫn file dữ liệu CSV
        self.file_path = os.path.join("dataset", "customerin4.csv")

        # Kết nối sự kiện nút bấm
        self.ui.pushButtonLogin.clicked.connect(self.handle_login)
        self.ui.pushButtonRegister.clicked.connect(self.open_register_window)
        self.ui.pushButtonForgot.clicked.connect(self.open_forgot_window)
        self.ui.eyeBtn.clicked.connect(self.toggle_password_visibility)

    def handle_login(self):
        """Kiểm tra tài khoản, mật khẩu và điều khoản """
        email_input = self.ui.lineEditEmail.text().strip()
        password_input = self.ui.lineEditPass.text().strip()

        # 1. KIỂM TRA NÚT TÍCH ĐIỀU KHOẢN (MỚI THÊM)
        if not self.ui.checkBoxTerms.isChecked():
            QMessageBox.warning(self, "Thông báo", "Bạn phải đồng ý với các điều khoản và chính sách để đăng nhập!")
            return

        # 2. Kiểm tra bỏ trống trường nhập liệu
        if not email_input or not password_input:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập Email và Mật khẩu!")
            return

        if not os.path.exists(self.file_path):
            QMessageBox.critical(self, "Lỗi", "Hệ thống chưa có dữ liệu người dùng!")
            return

        login_success = False
        user_name = ""
        try:
            with open(self.file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Email') == email_input and row.get('Mật khẩu') == password_input:
                        login_success = True
                        user_name = row.get('Họ và tên')
                        break
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc dữ liệu: {e}")
            return

        if login_success:
            QMessageBox.information(self, "Thành công", f"Chào mừng {user_name}!")
        else:
            QMessageBox.warning(self, "Thất bại", "Email hoặc Mật khẩu không đúng!")

    def open_forgot_window(self):
        """Mở màn hình Quên mật khẩu """
        try:
            from forgotPasswordMainWindowEx import ForgotPasswordWindow
            self.forgot_win = ForgotPasswordWindow()
            self.forgot_win.show()
            self.close()
        except ModuleNotFoundError:
            QMessageBox.critical(self, "Lỗi hệ thống", "Không tìm thấy file 'forgotPasswordMainWindowEx.py'!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở màn hình Quên mật khẩu: {e}")

    def open_register_window(self):
        """Mở màn hình Đăng ký """
        try:
            from registerMainWindowEx import RegisterWindow
            self.register_win = RegisterWindow()
            self.register_win.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở màn hình Đăng ký: {e}")

    def toggle_password_visibility(self):
        """Ẩn/Hiện mật khẩu """
        if self.ui.lineEditPass.echoMode() == QLineEdit.EchoMode.Password:
            self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Password)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginMainWindowEx()
    window.show()
    sys.exit(app.exec())
