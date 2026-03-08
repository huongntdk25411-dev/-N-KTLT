import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailService:
    @staticmethod
    def send_otp(receiver_email, otp_code):
        """Gửi mã xác thực qua SMTP Gmail"""
        # Cấu hình tài khoản gửi
        sender_email = "newyearphoto@gmail.com"  # Email tiệm New Year Photo
        app_password = "happynewyear8386"  # Mật khẩu

        # Tạo nội dung email
        msg = MIMEMultipart()
        msg['From'] = f"New Year Photo <{sender_email}>"
        msg['To'] = receiver_email
        msg['Subject'] = f"[{otp_code}] Mã xác thực tài khoản New Year Photo"

        body = f"""
        Chào bạn,

        Mã OTP để thiết lập lại mật khẩu của bạn là: {otp_code}
        Vui lòng nhập mã này vào ứng dụng để tiếp tục.

        Nếu không phải bạn thực hiện yêu cầu này, hãy bỏ qua email.
        """
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Kết nối server Gmail cổng 587
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Lỗi gửi mail: {e}")
            return False