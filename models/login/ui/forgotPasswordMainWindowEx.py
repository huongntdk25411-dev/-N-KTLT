import sys, os, csv, random, smtplib
from email.message import EmailMessage
from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtCore import Qt
from models.login.ui.forgotPasswordMainWindow import Ui_MainWindow


class ForgotPasswordWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Style ô email
        self.ui.lineEditEmail.setStyleSheet("""
            QLineEdit {
                border: 2px solid #FF9966;
                border-radius: 12px;
                padding-left: 15px;
                color: black;
                background-color: white;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 2px solid #FF6600;
                background-color: #FFFDFB;
            }
        """)

        # Style nút reset
        self.ui.pushButtonReset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.pushButtonReset.setStyleSheet("""
            QPushButton {
                background-color: #FF6600;
                color: white;
                font-weight: bold;
                font-size: 13pt;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #E65C00;
            }
            QPushButton:pressed {
                background-color: #CC5200;
            }
        """)

        self.sender_email = "newyearphoto8386@gmail.com"
        self.app_password = "jozz upku knjg nxke"

        self.file_path = self.get_data_path()

        self.ui.pushButtonReset.clicked.connect(self.handle_reset_process)

    def show_message(self, icon, title, text):

        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 11pt;
            }
            QPushButton {
                color: black;
                background-color: #f0f0f0;
                padding: 5px 20px;
                border-radius: 5px;
            }
        """)

        msg.exec()

    def get_data_path(self):

        current_dir = Path(__file__).resolve().parent
        potential_path = current_dir.parent.parent.parent / "datasets" / "customerin4.csv"

        if potential_path.exists():
            return potential_path

        fallback_path = current_dir / "datasets" / "customerin4.csv"
        os.makedirs(fallback_path.parent, exist_ok=True)

        return fallback_path

    def send_otp_via_email(self, receiver_email, otp_code):

        try:

            msg = EmailMessage()
            msg['Subject'] = f"[{otp_code}] Mã xác thực khôi phục mật khẩu - New Year Photo"
            msg['From'] = self.sender_email
            msg['To'] = receiver_email

            html_content = f"""
            <html>
            <body style="font-family: Arial;">

            <h2>New Year Photo</h2>

            <p>Mã OTP của bạn là:</p>

            <h1 style="color:#FF6600">{otp_code}</h1>

            <p>Mã có hiệu lực trong thời gian ngắn.</p>

            </body>
            </html>
            """

            msg.add_alternative(html_content, subtype='html')

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.sender_email, self.app_password)
                smtp.send_message(msg)

            return True

        except Exception as e:
            print("Lỗi gửi mail:", e)
            return False

    def handle_reset_process(self):

        email = self.ui.lineEditEmail.text().strip()

        if not email:
            self.show_message(QMessageBox.Icon.Warning, "Lỗi", "Vui lòng nhập email!")
            return

        email_found = False

        try:

            if self.file_path.exists():

                with open(self.file_path, 'r', encoding='utf-8-sig') as f:
                    reader = csv.reader(f)

                    for row in reader:

                        if len(row) > 2 and row[2].strip().lower() == email.lower():
                            email_found = True
                            break

            if email_found:

                otp_code = str(random.randint(100000, 999999))

                if self.send_otp_via_email(email, otp_code):

                    self.show_message(
                        QMessageBox.Icon.Information,
                        "Thành công",
                        f"Mã OTP đã gửi tới {email}"
                    )

                    try:

                        from models.login.ui.verifyOTPMainWindowEx import VerifyOTPWindow

                        self.verify_win = VerifyOTPWindow(email=email, otp=otp_code)
                        self.verify_win.show()
                        self.close()

                    except Exception as e:

                        self.show_message(
                            QMessageBox.Icon.Critical,
                            "Lỗi Import",
                            f"Lỗi mở màn hình Verify: {e}"
                        )

                else:

                    self.show_message(
                        QMessageBox.Icon.Critical,
                        "Lỗi",
                        "Gửi mail thất bại!"
                    )

            else:

                self.show_message(
                    QMessageBox.Icon.Warning,
                    "Lỗi",
                    "Email không tồn tại trong hệ thống!"
                )

        except Exception as e:

            self.show_message(
                QMessageBox.Icon.Critical,
                "Lỗi hệ thống",
                f"Lỗi: {e}"
            )
