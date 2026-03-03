import os
import csv

from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from models.login.ui.loginMainWindow import Ui_MainWindow
from ui.MainWindowEx import MainWindowEx


class LoginMainWindowEx(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ===== STYLE chữ đen - nền trắng =====
        self.ui.lineEditEmail.setStyleSheet(
            "QLineEdit { color: black; background-color: white; }"
        )

        self.ui.lineEditPass.setStyleSheet(
            "QLineEdit { color: black; background-color: white; }"
        )  # <-- ĐÃ THÊM DẤU ĐÓNG )

        # ===== Ẩn mật khẩu =====
        self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Password)

        # ===== Đường dẫn CSV =====

        # Tìm thư mục FINALPROJECT (thư mục chứa datasets)
        current_path = Path(__file__).resolve()

        for parent in current_path.parents:
            if (parent / "datasets").exists():
                PROJECT_ROOT = parent
                break

        self.file_path = PROJECT_ROOT / "datasets" / "customerin4.csv"

        print("CSV PATH:", self.file_path)

        print("CSV PATH:", self.file_path)

        # ===== Sự kiện =====
        self.ui.pushButtonLogin.clicked.connect(self.handle_login)
        self.ui.eyeBtn.clicked.connect(self.toggle_password_visibility)

    def handle_login(self):
        email_input = self.ui.lineEditEmail.text().strip()
        password_input = self.ui.lineEditPass.text().strip()

        if not email_input or not password_input:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not os.path.exists(self.file_path):
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy file customerin4.csv")
            return

        with open(self.file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row['Email'].strip().lower() == email_input.lower()
                        and row['Mật khẩu'].strip() == password_input):

                    QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")

                    self.main_win = MainWindowEx(user_email=email_input)
                    self.main_win.show()
                    self.close()
                    return

        QMessageBox.warning(self, "Thất bại", "Email hoặc mật khẩu không đúng!")

    def toggle_password_visibility(self):
        if self.ui.lineEditPass.echoMode() == QLineEdit.EchoMode.Password:
            self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.lineEditPass.setEchoMode(QLineEdit.EchoMode.Password)