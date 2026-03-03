import sys
import os
import csv
import random
import smtplib
from email.message import EmailMessage
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt6.QtCore import QTimer
from forgotPasswordMainWindow import Ui_MainWindow
from loginMainWindowEx import LoginMainWindowEx


class ForgotPasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # CỐ ĐỊNH MÀU CHỮ ĐEN CHO Ô NHẬP LIỆU (Tránh lỗi Dark Mode)
        # Lấy stylesheet hiện tại và nối thêm thuộc tính color: black
        self.ui.lineEditEmail.setStyleSheet(self.ui.lineEditEmail.styleSheet() + "color: black;")

        # --- CẤU HÌNH GỬI MAIL ---
        self.sender_email = "newyearphoto8386@gmail.com"
        self.app_password = "jozz upku knjg nxke"

        # Đường dẫn file dữ liệu
        self.file_path = os.path.join("dataset", "customerin4.csv")
        self.current_otp = None

        # Cấu hình bộ đếm ngược 60s
        self.count = 60
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)

        # Kết nối sự kiện nút bấm
        self.ui.pushButtonReset.clicked.connect(self.handle_forgot_process)
        self.ui.pushButtonBack.clicked.connect(self.handle_back)

    def send_otp_via_email(self, receiver_email, otp_code):
        """Hàm gửi email định dạng HTML chuyên nghiệp"""
        try:
            msg = EmailMessage()
            msg['Subject'] = f"[{otp_code}] Mã xác thực khôi phục mật khẩu - New Year Photo"
            msg['From'] = self.sender_email
            msg['To'] = receiver_email

            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
                        <div style="background-color: #FF6600; padding: 20px; text-align: center;">
                            <h1 style="color: white; margin: 0;">New Year Photo</h1>
                        </div>
                        <div style="padding: 30px;">
                            <p>Xin chào,</p>
                            <p>Bạn đã yêu cầu lấy lại mật khẩu. Mã xác thực (OTP) của bạn là:</p>
                            <div style="text-align: center; margin: 30px 0;">
                                <span style="font-size: 32px; font-weight: bold; color: #FF6600; letter-spacing: 5px; border: 2px dashed #FF6600; padding: 10px 20px;">
                                    {otp_code}
                                </span>
                            </div>
                            <p style="font-size: 14px; color: #666;"><i>Lưu ý: Mã này chỉ có hiệu lực trong thời gian ngắn. Tuyệt đối không chia sẻ mã cho người khác.</i></p>
                            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                            <p>Trân trọng,<br><strong>Đội ngũ New Year Photo</strong></p>
                        </div>
                    </div>
                </body>
            </html>
            """
            msg.add_alternative(html_content, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"Lỗi gửi mail: {e}")
            return False

    def handle_forgot_process(self):
        """Xử lý khi nhấn nút Đặt lại mật khẩu"""
        email_input = self.ui.lineEditEmail.text().strip()

        if not email_input:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Email để nhận mã OTP!")
            return

        user_data = None
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Email') == email_input:
                        user_data = row
                        break

        if not user_data:
            QMessageBox.warning(self, "Lỗi", "Email này chưa được đăng ký trong hệ thống!")
            return

        self.current_otp = str(random.randint(100000, 999999))
        if self.send_otp_via_email(email_input, self.current_otp):
            QMessageBox.information(self, "Thành công", f"Mã OTP đã được gửi đến:\n{email_input}")
            self.start_countdown()
            self.verify_otp(user_data)
        else:
            QMessageBox.critical(self, "Lỗi",
                                 "Không thể gửi Email. Hãy kiểm tra kết nối hoặc cấu hình mật khẩu ứng dụng!")

    def start_countdown(self):
        self.ui.pushButtonReset.setEnabled(False)
        self.count = 60
        self.timer.start(1000)

    def update_countdown(self):
        self.count -= 1
        if self.count > 0:
            self.ui.pushButtonReset.setText(f"Gửi lại sau ({self.count}s)")
        else:
            self.timer.stop()
            self.ui.pushButtonReset.setEnabled(True)
            self.ui.pushButtonReset.setText("Đặt lại mật khẩu")

    def verify_otp(self, user_data):
        """Hộp thoại xác thực OTP và hiển thị mật khẩu"""
        otp_input, ok = QInputDialog.getText(self, "Xác thực OTP", "Vui lòng nhập mã 6 số:")
        if ok and otp_input:
            if otp_input == self.current_otp:
                res = (
                    f"Xác thực thành công!\n\n"
                    f"Tên đăng nhập: {user_data.get('Tên đăng nhập', 'N/A')}\n"
                    f"Mật khẩu của bạn là: {user_data.get('Mật khẩu', 'N/A')}"
                )
                QMessageBox.information(self, "Thông tin khôi phục", res)
            else:
                QMessageBox.warning(self, "Lỗi", "Mã OTP không chính xác. Vui lòng kiểm tra lại!")

    def handle_back(self):
        self.login_win = LoginMainWindowEx()
        self.login_win.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ForgotPasswordWindow()
    window.show()
    sys.exit(app.exec())