import sys, os, csv, re
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QTextBrowser, \
    QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from models.login.ui.registerMainWindow import Ui_MainWindow


class TermsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Điều khoản & Chính sách - New Year Photo")
        self.resize(500, 600)
        self.setStyleSheet("background-color: white; border-radius: 10px;")

        layout = QVBoxLayout(self)

        title = QLabel("ĐIỀU KHOẢN & CHÍNH SÁCH DỊCH VỤ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #A5361B; margin: 10px;")
        layout.addWidget(title)

        # Nội dung chính sách
        self.textBrowser = QTextBrowser()
        self.textBrowser.setHtml("""
            <div style='color: #2c3e50; font-family: "Segoe UI", sans-serif; line-height: 1.6;'>
                <p style='text-align: center; font-style: italic; color: #7f8c8d;'>Chào mừng bạn đến với New Year Photo - Nơi lưu giữ khoảnh khắc rạng rỡ.</p>

                <hr style='border: 0; border-top: 1px solid #FF9966;'>

                <h3 style='color: #d35400;'>1. Quyền sở hữu và sử dụng hình ảnh</h3>
                <ul>
                    <li>Tất cả sản phẩm hình ảnh sau khi hoàn thiện thuộc quyền sở hữu cá nhân của khách hàng.</li>
                    <li><b>New Year Photo</b> cam kết không sử dụng hình ảnh của quý khách cho mục đích quảng cáo nếu chưa được sự đồng ý.</li>
                </ul>

                <h3 style='color: #d35400;'>2. Quy định đặt lịch và thanh toán</h3>
                <ul>
                    <li>Quý khách vui lòng có mặt đúng giờ hẹn. Việc trễ quá <b>15 phút</b> có thể làm ảnh hưởng đến thời lượng buổi chụp của quý khách.</li>
                    <li>Đối với các yêu cầu thực hiện bộ ảnh tại địa điểm ngoài cơ sở của studio, Quý khách vui lòng hỗ trợ thêm chi phí di chuyển và vận chuyển thiết bị cho ekip để đảm bảo chất lượng phục vụ tốt nhất.</li>
                    <li>Khoản đặt cọc sẽ không được hoàn lại nếu quý khách hủy lịch trong vòng 48 giờ trước giờ chụp.</li>
                </ul>

                <h3 style='color: #d35400;'>3. Bảo mật thông tin cá nhân</h3>
                <ul>
                    <li>Chúng tôi thu thập các thông tin (Họ tên, Email) chỉ để phục vụ việc quản lý hồ sơ và gửi trả ảnh chụp.</li>
                    <li>Dữ liệu cá nhân của quý khách được bảo mật tuyệt đối trên hệ thống nội bộ của tiệm.</li>
                </ul>

                <h3 style='color: #d35400;'>4. Trách nhiệm của khách hàng</h3>
                <ul>
                    <li>Vui lòng bảo quản tài sản cá nhân trong suốt quá trình sử dụng dịch vụ tại studio.</li>
                    <li>Khách hàng có trách nhiệm bồi thường nếu gây hư hỏng thiết bị hoặc bối cảnh chụp do sử dụng sai mục đích.</li>
                </ul>

                <p style='margin-top: 20px; border-left: 4px solid #FF6600; padding-left: 10px; background-color: #fff5f0;'>
                    <b>Lưu ý:</b> Bằng việc nhấn nút <b>"Tôi đã đọc và đồng ý"</b>, bạn xác nhận đã hiểu rõ và chấp nhận toàn bộ các điều khoản nêu trên.
                </p>

                <p style='text-align: center; color: #7f8c8d; font-size: 10pt; margin-top: 20px;'>
                    <i>Cảm ơn bạn đã lựa chọn New Year Photo!</i>
                </p>
            </div>
        """)
        self.textBrowser.setStyleSheet("""
            QTextBrowser {
                border: 1px solid #FF9966; 
                border-radius: 8px; 
                padding: 15px;
                background-color: #fcfcfc;
            }
        """)
        layout.addWidget(self.textBrowser)

        # Nút xác nhận đồng ý
        self.btnAccept = QPushButton("Tôi đã đọc và đồng ý")
        self.btnAccept.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btnAccept.setStyleSheet("""
            QPushButton {
                background-color: #FF6600; 
                color: white; 
                font-weight: bold; 
                height: 45px; 
                border-radius: 12px;
                font-size: 11pt;
            }
            QPushButton:hover { background-color: #E65C00; }
        """)
        self.btnAccept.clicked.connect(self.accept)
        layout.addWidget(self.btnAccept)

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Thiết lập đường dẫn dữ liệu [cite: 25, 26]
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.abspath(os.path.join(self.current_dir, "..", "..", ".."))
        self.dataset_path = os.path.join(self.root_dir, "datasets", "customerin4.csv")
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)

        self.init_ui_config()
        self.setup_signals()

    def init_ui_config(self):
        # Ép chữ đen cho các ô nhập để hiển thị rõ
        style = "color: black; border: 2px solid #FF9966; border-radius: 12px; padding-left: 15px; background: white;"
        for w in [self.ui.lineEditName, self.ui.lineEditEmail, self.ui.lineEditUser, self.ui.lineEditPass,
                  self.ui.lineEditBirthday]:
            w.setStyleSheet(style)

        # Sửa lỗi AttributeError: Sử dụng setAutoExclusive thay vì setExclusive [cite: 52]
        for btn in [self.ui.radMale, self.ui.radFemale, self.ui.radFemale_2]:
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

        self.ui.checkBoxTerms.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.pushButtonRegister1.setEnabled(False)

        # Bỏ chọn mặc định [cite: 52]
        self.ui.radMale.setChecked(False)
        self.ui.radFemale.setChecked(False)
        self.ui.radFemale_2.setChecked(False)

        # Bật lại để chỉ được chọn 1
        self.ui.radMale.setAutoExclusive(True)
        self.ui.radFemale.setAutoExclusive(True)
        self.ui.radFemale_2.setAutoExclusive(True)

        self.ui.checkBoxTerms.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.pushButtonRegister1.setEnabled(False)

    def setup_signals(self):
        self.ui.checkBoxTerms.stateChanged.connect(self.toggle_btn)
        self.ui.pushButtonRegister1.clicked.connect(self.handle_reg)
        self.ui.pushButtonBack1.clicked.connect(self.handle_back)

        # Kết nối sự kiện cho các nút giới tính
        self.ui.radMale.clicked.connect(self.show_terms_popup)
        self.ui.radFemale.clicked.connect(self.show_terms_popup)
        self.ui.radFemale_2.clicked.connect(self.show_terms_popup)

        # Tự động thêm dấu "/" khi gõ ngày sinh
        self.ui.lineEditBirthday.textChanged.connect(self.format_birthday)

    def format_birthday(self, text):
        """Tự động chèn dấu / định dạng dd/mm/yyyy"""
        # Giữ lại các ký tự số
        digits = "".join(filter(str.isdigit, text))
        if len(digits) > 8: digits = digits[:8]

        formatted = ""
        if len(digits) > 0: formatted += digits[:2]
        if len(digits) > 2: formatted += "/" + digits[2:4]
        if len(digits) > 4: formatted += "/" + digits[4:]

        # Chặn tín hiệu để tránh lặp vô tận
        self.ui.lineEditBirthday.blockSignals(True)
        self.ui.lineEditBirthday.setText(formatted)
        self.ui.lineEditBirthday.blockSignals(False)

    def show_message(self, title, text, icon, auto_back=False):
        """Hiển thị thông báo chữ đen và xử lý điều hướng """
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        # Ép CSS chữ đen cho Label và Button
        msg.setStyleSheet("QLabel{ color: black; font-size: 11pt; } QPushButton{ color: black; min-width: 80px; }")
        msg.exec()
        if auto_back:
            self.handle_back()

    def get_next_stt(self):
        """Khắc phục lỗi thiếu hàm lấy STT """
        if not os.path.exists(self.dataset_path):
            return 1
        try:
            with open(self.dataset_path, 'r', encoding='utf-8-sig') as f:
                lines = list(csv.reader(f))
                if len(lines) <= 1: return 1
                return int(lines[-1][0]) + 1
        except:
            return 1

    def show_terms_popup(self):
        if TermsDialog(self).exec() == QDialog.DialogCode.Accepted:
            self.ui.checkBoxTerms.setChecked(True)
        else:
            # Nếu không đồng ý thì bỏ chọn radio button
            self.ui.radMale.setAutoExclusive(False)
            self.ui.radFemale.setAutoExclusive(False)
            self.ui.radFemale_2.setAutoExclusive(False)
            self.ui.radMale.setChecked(False)
            self.ui.radFemale.setChecked(False)
            self.ui.radFemale_2.setChecked(False)
            self.ui.radMale.setAutoExclusive(True)
            self.ui.radFemale.setAutoExclusive(True)
            self.ui.radFemale_2.setAutoExclusive(True)
            self.ui.checkBoxTerms.setChecked(False)

    def toggle_btn(self):
        ready = self.ui.checkBoxTerms.isChecked()
        self.ui.pushButtonRegister1.setEnabled(ready)
        bg = "#FF6600" if ready else "#ccc"
        self.ui.pushButtonRegister1.setStyleSheet(
            f"background-color: {bg}; color: white; font-weight: bold; border-radius: 15px;")

    def handle_reg(self):
        name = self.ui.lineEditName.text().strip()
        email = self.ui.lineEditEmail.text().strip()
        phone = self.ui.lineEditUser.text().strip()
        birthday = self.ui.lineEditBirthday.text().strip()
        password = self.ui.lineEditPass.text().strip()


        gender = "Nam" if self.ui.radMale.isChecked() else "Nữ" if self.ui.radFemale.isChecked() else "Khác"

        if not all([name, email, phone, birthday, password]):
            return self.show_message("Lỗi", "Vui lòng điền đầy đủ thông tin!", QMessageBox.Icon.Warning)

        if not phone.isdigit():
            return self.show_message("Lỗi", "Số điện thoại chỉ được chứa ký tự số!", QMessageBox.Icon.Warning)

        if not re.match(r"^\d{2}/\d{2}/\d{4}$", birthday):
            return self.show_message("Lỗi", "Ngày sinh phải đúng định dạng dd/mm/yyyy!", QMessageBox.Icon.Warning)

        if len(password) < 6:
            return self.show_message("Lỗi", "Mật khẩu phải từ 6 ký tự!", QMessageBox.Icon.Warning)

        # 3. Ghi dữ liệu vào file CSV
        try:
            # Lấy STT
            stt = self.get_next_stt()

            file_exists = os.path.isfile(self.dataset_path)

            with open(self.dataset_path, 'a', newline='', encoding='utf-8-sig') as f:
                fieldnames = ["STT", "Họ và tên", "Email", "Số điện thoại", "Ngày tháng năm sinh", "Giới tính",
                              "Mật khẩu"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                writer.writerow({
                    "STT": stt,
                    "Họ và tên": name,
                    "Email": email,
                    "Số điện thoại": phone,
                    "Ngày tháng năm sinh": birthday,
                    "Giới tính": gender,
                    "Mật khẩu": password
                })

            self.show_message("Thành công", "Đăng ký thành công!", QMessageBox.Icon.Information, auto_back=True)

        except Exception as e:
            self.show_message("Lỗi", f"Lỗi hệ thống khi ghi file: {e}", QMessageBox.Icon.Critical)
    def handle_back(self):
        from models.login.ui.loginMainWindowEx import LoginMainWindowEx
        self.login = LoginMainWindowEx()
        self.login.show()
        self.close()



