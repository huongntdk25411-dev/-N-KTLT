import csv
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from models.user.UserManagerEx import UserManagerEx
from models.user.tabAccount.accountmanager import AccountManager
from models.user.tabAccount.feature_update_info.ui_Account.UpdateProfileDialogExt import UpdateProfileDialogExt
from ui.MainWindow import Ui_MainWindow

from models.user.booking import Booking


class MainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, user_email=None):
        super().__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        # Đường dẫn bookings.json
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
        self.json_path = os.path.join(PROJECT_ROOT, "datasets", "bookings.json")

        self.booking = Booking(self)
        self.usermanager=UserManagerEx(self)

        # Quản lý tài khoản
        if user_email:
            self.account_manager = AccountManager(self, user_email)

        self.filepath="D:/-N-KTLT/datasets/customerin4.csv"
        self.setupSignalAndSlot()

        # lưu mail người dùng hiện tại
        self.user_email = user_email
        self.current_user_data = {}
        # Tải dữ liệu khi vừa mở form
        if self.user_email:
            self.load_profile()
    def setupSignalAndSlot(self):
        self.btnUpdate.clicked.connect(self.processUpdate)
        self.btnDeleteAccount.clicked.connect(self.processDeleteAccount)
    def processUpdate(self):
        dlg = UpdateProfileDialogExt(self.user_email)
        result = dlg.exec()

        if result:  # if push Confirm Button (accepted)
            # read file after update
            self.load_profile()

    def load_profile(self):
        with open(self.filepath,"r",encoding="utf-8-sig") as f:
            reader=csv.DictReader(f)
            self.csv_headers=reader.fieldnames
            self.all_users=list(reader)
        for user in self.all_users:
            if user.get("Email") == self.user_email:
                self.current_user_data = user
                break
        # sau khi tìm thấy user, gọi hàm để hiển thị dữ liệu len form
        self.display_profile()
    def display_profile(self):
        # 1. Lấy thông tin có sẵn
        name = self.current_user_data.get("Họ và tên", "")
        email = self.current_user_data.get("Email", "")
        username = self.current_user_data.get("Tên đăng nhập", "")

        # 2. Xử lý giá trị mặc định cho các mục trống
        phone = self.current_user_data.get("Số điện thoại", "").strip()
        phone = phone if phone else "Chưa có thông tin"

        dob = self.current_user_data.get("Ngày sinh", "").strip()
        dob = dob if dob else "1/1/1999"

        gender = self.current_user_data.get("Giới tính", "").strip()
        gender = gender if gender else "Khác"

        # 3. Đưa thông tin lên giao diện
        self.lblName.setText(name)
        self.lblEmail.setText(email)
        self.lblPhone.setText(phone)
        self.lblDOB.setText(dob)
        self.lblGender.setText(gender)
        self.labelUserName.setText(username)
    def processDeleteAccount(self):
        #1. hiện thông báo xác nhận xóa
        reply=QMessageBox.question(self,"Xác nhận xóa","Bạn có chắc chắn muốn xóa tài khoản này không?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        #2. nếu chọn yes
        if reply == QMessageBox.StandardButton.Yes:
            # loại bỏ account hịện tại ra khỏi danh sách
            self.all_users=[user for user in self.all_users if user.get("Email") != self.user_email]
            # cập nhật lại vào file csv
            with open(self.filepath,"w",encoding="utf-8-sig",newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.csv_headers)
                writer.writeheader()
                writer.writerows(self.all_users)
            QMessageBox.information(self, "Thành công", "Tài khoản của bạn đã được xóa thành công!")
            #3. đóng mainwindow hiện tại
            self.close()
            #4. trở về màn hình đăng nhập
            from models.login.ui.loginMainWindowEx import LoginMainWindowEx
            self.login_window=LoginMainWindowEx()
            self.login_window.show()
