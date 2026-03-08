import os
import csv
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QLineEdit

from models.login.ui.loginMainWindow import Ui_MainWindow
from ui.AdminMainwindow.AdminMainwindowEx import AdminMainwindowEx


class LoginMainWindowEx(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.checkBoxTerms.setStyleSheet("""
        QCheckBox {
            color: #555;
            font-size: 12px;
        }

        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid #ff8c00;
            border-radius: 4px;
            background: white;
        }

        QCheckBox::indicator:checked {
            background-color: #ff8c00;
            border: 2px solid #ff8c00;
        }
        """)
        # đường dẫn file dữ liệu
        self.file_path = self.get_data_path()

        # connect các nút
        self.ui.pushButtonLogin.clicked.connect(self.handle_login)
        self.ui.pushButtonRegister.clicked.connect(self.open_register)
        self.ui.pushButtonForgot.clicked.connect(self.open_forgot_password)
        self.ui.eyeBtn.clicked.connect(self.toggle_password_visibility)

    # lấy đường dẫn file csv
    def get_data_path(self):
        project_root = Path(__file__).resolve().parents[3]
        return project_root / "datasets" / "customerin4.csv"

    # xử lý đăng nhập
    def handle_login(self):

        email = self.ui.lineEditEmail.text().strip()
        password = self.ui.lineEditPass.text().strip()

        # đăng nhập admin
        if email == "admin@gmail.com" and password == "admin":

            self.admin_window = AdminMainwindowEx()
            self.admin_window.show()

            self.close()
            return

        # kiểm tra nhập liệu
        if not email or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # kiểm tra điều khoản
        if not self.ui.checkBoxTerms.isChecked():
            QMessageBox.warning(self, "Điều khoản", "Bạn chưa đồng ý với điều khoản!")
            return

        try:

            found = False

            with open(self.file_path, "r", encoding="utf-8-sig") as f:

                reader = csv.reader(f)

                for row in reader:

                    if len(row) > 6:

                        user_email = row[2].strip().lower()
                        user_password = row[6].strip()

                        if user_email == email.lower() and user_password == password:
                            found = True
                            break

            # nếu tìm thấy tài khoản
            if found:

                QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")

                from ui.UserMainwindow.MainWindowEx import MainWindowEx

                self.main_window = MainWindowEx(user_email=email)
                self.main_window.show()

                self.close()

            else:
                QMessageBox.warning(self, "Thất bại", "Email hoặc mật khẩu không chính xác!")

        except Exception as e:

            QMessageBox.critical(self, "Lỗi", str(e))

    # hiển thị / ẩn mật khẩu
    def toggle_password_visibility(self):

        if self.ui.lineEditPass.echoMode() == QLineEdit.EchoMode.Password:
            self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Password)

    # mở cửa sổ đăng ký
    def open_register(self):

        from models.login.ui.registerMainWindowEx import RegisterWindow

        self.register_window = RegisterWindow()
        self.register_window.show()

        self.close()

    # mở cửa sổ quên mật khẩu
    def open_forgot_password(self):

        from models.login.ui.forgotPasswordMainWindowEx import ForgotPasswordWindow

        self.forgot_window = ForgotPasswordWindow()
        self.forgot_window.show()

        self.close()


