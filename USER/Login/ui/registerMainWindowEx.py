import sys, os, csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from registerMainWindow import Ui_MainWindow


class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Thiết lập file & folder
        self.path = "dataset/customerin4.csv"
        os.makedirs("dataset", exist_ok=True)

        # UI Setup: Chữ đen & Khóa nút
        for w in [self.ui.lineEditName, self.ui.lineEditEmail, self.ui.lineEditUser, self.ui.lineEditPass]:
            w.setStyleSheet(w.styleSheet() + "color: black;")

        self.ui.pushButtonRegister1.setEnabled(False)

        # Kết nối sự kiện
        self.ui.checkBoxTerms.stateChanged.connect(self.toggle_btn)
        self.ui.pushButtonRegister1.clicked.connect(self.handle_reg)
        self.ui.pushButtonBack1.clicked.connect(self.handle_back)

    def toggle_btn(self):
        ready = self.ui.checkBoxTerms.isChecked()
        self.ui.pushButtonRegister1.setEnabled(ready)
        bg = "#FF6600" if ready else "#ccc"
        self.ui.pushButtonRegister1.setStyleSheet(
            f"background-color: {bg}; color: white; font-weight: bold; font-size: 14pt; border-radius: 15px;")

    def handle_reg(self):
        d = {
            "Họ và tên": self.ui.lineEditName.text().strip(),
            "Email": self.ui.lineEditEmail.text().strip(),
            "Tên đăng nhập": self.ui.lineEditUser.text().strip(),
            "Mật khẩu": self.ui.lineEditPass.text().strip(),
            "Giới tính": "Nam" if self.ui.radMale.isChecked() else "Nữ"
        }

        if not all(list(d.values())[:-1]): return QMessageBox.warning(self, "Lỗi", "Nhập thiếu thông tin!")
        if len(d["Mật khẩu"]) < 6: return QMessageBox.warning(self, "Lỗi", "Mật khẩu ít nhất 6 ký tự!")

        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8-sig') as f:
                rows = list(csv.DictReader(f))
                if any(r['Email'] == d['Email'] for r in rows): return QMessageBox.warning(self, "Lỗi",
                                                                                           "Email đã tồn tại!")
                if any(r['Tên đăng nhập'] == d['Tên đăng nhập'] for r in rows): return QMessageBox.warning(self, "Lỗi",
                                                                                                           "Username tồn tại!")

        try:
            new = not os.path.exists(self.path)
            with open(self.path, 'a', newline='', encoding='utf-8-sig') as f:
                w = csv.DictWriter(f, fieldnames=d.keys())
                if new: w.writeheader()
                w.writerow(d)
            QMessageBox.information(self, "Xong", "Đăng ký thành công!")
            self.handle_back()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi lưu file: {e}")

    def handle_back(self):
        try:
            from loginMainWindowEx import LoginMainWindowEx
            self.login = LoginMainWindowEx()
            self.login.show()
            self.close()
        except Exception as e:
            print(f"Lỗi chuyển màn hình: {e}")
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Thêm dòng này để nếu lỗi ảnh nó vẫn chạy tiếp
    app.setStyle("Fusion")
    win = RegisterWindow()
    win.show()
    sys.exit(app.exec())
