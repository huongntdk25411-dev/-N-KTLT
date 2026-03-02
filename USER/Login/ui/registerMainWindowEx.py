import sys, os, csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QLabel, QTextBrowser, \
    QPushButton
from PyQt6.QtCore import Qt
from registerMainWindow import Ui_MainWindow


class TermsDialog(QDialog):
    """Cửa sổ Pop-up Điều khoản và Chính sách"""

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

                <h3 style='color: #d35400;'>1. Quyền sở hữu và Sử dụng hình ảnh</h3>
                <ul>
                    <li>Tất cả sản phẩm hình ảnh sau khi hoàn thiện thuộc quyền sở hữu cá nhân của khách hàng.</li>
                    <li><b>New Year Photo</b> cam kết không sử dụng hình ảnh của quý khách cho mục đích quảng cáo nếu chưa được sự đồng ý.</li>
                </ul>

                <h3 style='color: #d35400;'>2. Quy định Đặt lịch và Thanh toán</h3>
                <ul>
                    <li>Quý khách vui lòng có mặt đúng giờ hẹn. Việc trễ quá <b>15 phút</b> có thể làm ảnh hưởng đến thời lượng buổi chụp của quý khách.</li>
                    <li>Khoản đặt cọc sẽ không được hoàn lại nếu quý khách hủy lịch trong vòng 24 giờ trước giờ chụp.</li>
                </ul>

                <h3 style='color: #d35400;'>3. Bảo mật Thông tin Cá nhân</h3>
                <ul>
                    <li>Chúng tôi thu thập các thông tin (Họ tên, Email) chỉ để phục vụ việc quản lý hồ sơ và gửi trả ảnh chụp.</li>
                    <li>Dữ liệu cá nhân của quý khách được bảo mật tuyệt đối trên hệ thống nội bộ của tiệm.</li>
                </ul>

                <h3 style='color: #d35400;'>4. Trách nhiệm của Khách hàng</h3>
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

        # Thiết lập file & folder
        self.path = "dataset/customerin4.csv"
        os.makedirs("dataset", exist_ok=True)

        # UI Setup
        for w in [self.ui.lineEditName, self.ui.lineEditEmail, self.ui.lineEditUser, self.ui.lineEditPass]:
            w.setStyleSheet(w.styleSheet() + "color: black;")

        # Chặn click tay vào checkbox để bắt buộc phải chọn giới tính trước
        self.ui.checkBoxTerms.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.pushButtonRegister.setEnabled(False)

        # Kết nối
        self.ui.checkBoxTerms.stateChanged.connect(self.toggle_btn)
        self.ui.pushButtonRegister.clicked.connect(self.handle_reg)
        self.ui.pushButtonBack.clicked.connect(self.handle_back)

        # Logic hiển thị Pop-up khi chọn giới tính
        self.ui.radMale.clicked.connect(self.show_terms_popup)
        self.ui.radFemale.clicked.connect(self.show_terms_popup)

    def show_terms_popup(self):
        """Hiển thị pop-up khi nhấn chọn giới tính"""
        dialog = TermsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Nếu nhấn nút Đồng ý trên pop-up
            self.ui.checkBoxTerms.setChecked(True)
        else:
            # Nếu tắt pop-up mà không đồng ý, hủy chọn giới tính
            self.ui.genderGroup.setExclusive(False)
            self.ui.radMale.setChecked(False)
            self.ui.radFemale.setChecked(False)
            self.ui.genderGroup.setExclusive(True)
            self.ui.checkBoxTerms.setChecked(False)

    def toggle_btn(self):
        """Thay đổi trạng thái nút đăng ký dựa trên checkbox điều khoản"""
        ready = self.ui.checkBoxTerms.isChecked()
        self.ui.pushButtonRegister.setEnabled(ready)
        bg = "#FF6600" if ready else "#ccc"
        self.ui.pushButtonRegister.setStyleSheet(
            f"background-color: {bg}; color: white; font-weight: bold; font-size: 14pt; border-radius: 15px;")

    def handle_reg(self):
        d = {
            "Họ và tên": self.ui.lineEditName.text().strip(),
            "Email": self.ui.lineEditEmail.text().strip(),
            "Tên đăng nhập": self.ui.lineEditUser.text().strip(),
            "Mật khẩu": self.ui.lineEditPass.text().strip(),
            "Giới tính": "Nam" if self.ui.radMale.isChecked() else "Nữ"
        }

        if not all(list(d.values())[:-1]): return QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        if len(d["Mật khẩu"]) < 6: return QMessageBox.warning(self, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")

        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8-sig') as f:
                rows = list(csv.DictReader(f))
                if any(r['Email'] == d['Email'] for r in rows):
                    return QMessageBox.warning(self, "Lỗi", "Email này đã được sử dụng!")
                if any(r['Tên đăng nhập'] == d['Tên đăng nhập'] for r in rows):
                    return QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại!")

        try:
            new = not os.path.exists(self.path)
            with open(self.path, 'a', newline='', encoding='utf-8-sig') as f:
                w = csv.DictWriter(f, fieldnames=d.keys())
                if new: w.writeheader()
                w.writerow(d)
            QMessageBox.information(self, "Thành công", "Tài khoản của bạn đã được đăng ký thành công!")
            self.handle_back()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Không thể lưu thông tin: {e}")

    def handle_back(self):
        """Quay lại màn hình đăng nhập"""
        try:
            from loginMainWindowEx import LoginMainWindowEx
            self.login = LoginMainWindowEx()
            self.login.show()
            self.close()
        except Exception as e:
            print(f"Lỗi khi chuyển đổi màn hình: {e}")
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = RegisterWindow()
    win.show()
    sys.exit(app.exec())
