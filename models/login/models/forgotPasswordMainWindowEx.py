import sys
import os
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
# Nhập class Ui_MainWindow từ file giao diện của bạn
from models.login.ui.forgotPasswordMainWindow import Ui_MainWindow


class ForgotPasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Đường dẫn đến file dữ liệu để kiểm tra email
        self.file_path = os.path.join("dataset", "customerin4.csv")

        # Kết nối sự kiện cho các nút bấm
        self.ui.pushButtonReset.clicked.connect(self.handle_reset_password)
        self.ui.pushButtonBack.clicked.connect(self.handle_back)

    def handle_reset_password(self):
        email_input = self.ui.lineEditEmail.text().strip()

        # 1. Kiểm tra nếu để trống
        if not email_input:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Email để đặt lại mật khẩu!")
            return

        # 2. Kiểm tra email có tồn tại trong hệ thống (file CSV) không
        found = False
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, mode='r', encoding='utf-8-sig') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row['Email'] == email_input:
                            found = True
                            password = row['Mật khẩu']
                            break
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đọc dữ liệu: {e}")
                return
        else:
            QMessageBox.warning(self, "Thông báo", "Hệ thống chưa có dữ liệu người dùng nào!")
            return

        # 3. Hiển thị kết quả
        if found:
            # Ở đây mình mô phỏng việc tìm lại mật khẩu cũ
            msg = (
                f"Yêu cầu thành công!\n\n"
                f"Hệ thống đã xác nhận email: {email_input}\n"
                f"Mật khẩu của bạn là: {password}"
            )
            QMessageBox.information(self, "Khôi phục mật khẩu", msg)
        else:
            QMessageBox.warning(self, "Lỗi", "Email này chưa được đăng ký trong hệ thống!")

    def handle_back(self):
        print("Quay lại màn hình đăng nhập...")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForgotPasswordWindow()
    window.show()
    sys.exit(app.exec())