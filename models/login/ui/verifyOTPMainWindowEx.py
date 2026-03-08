import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from models.login.ui.verifyOTPMainWindow import Ui_MainWindow


class VerifyOTPWindow(QMainWindow):
    def __init__(self, email, otp):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_email = email
        self.correct_otp = otp

        self.ui.labelInfo.setText(
            f"Mã xác thực đã được gửi đến:\n{self.user_email}"
        )

        self.ui.pushButtonVerify.clicked.connect(self.handle_verify)
        self.ui.pushButtonResend.clicked.connect(self.handle_resend)

    def handle_verify(self):
        input_otp = self.ui.lineEditOTP.text().strip()

        if not input_otp:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã OTP!")
            return

        if input_otp == self.correct_otp:
            QMessageBox.information(self, "Thành công", "Xác thực mã OTP thành công!")

            try:
                from models.login.ui.resetPasswordMainWindowEx import ResetPasswordWindow

                self.reset_win = ResetPasswordWindow(email=self.user_email)
                self.reset_win.show()
                self.close()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Lỗi",
                    f"Không thể mở màn hình Reset Password:\n{str(e)}"
                )

        else:
            QMessageBox.warning(
                self,
                "Thất bại",
                "Mã xác thực không chính xác. Vui lòng kiểm tra lại!"
            )

    def handle_resend(self):

        import random

        self.correct_otp = str(random.randint(100000, 999999))

        try:
            self.send_otp_email(self.user_email, self.correct_otp)

            QMessageBox.information(
                self,
                "Thông báo",
                "Mã OTP mới đã được gửi lại email của bạn."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Lỗi",
                f"Gửi mail thất bại: {e}"
            )

    def send_otp_email(self, email, otp):
        import smtplib
        from email.message import EmailMessage

        sender = "newyearphoto8386@gmail.com"
        password = "jozz upku knjg nxke"

        msg = EmailMessage()
        msg["Subject"] = "Mã OTP xác thực - New Year Photo"
        msg["From"] = sender
        msg["To"] = email

        msg.set_content(f"Mã OTP của bạn là: {otp}")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerifyOTPWindow("test@gmail.com", "123456")
    window.show()
    sys.exit(app.exec())