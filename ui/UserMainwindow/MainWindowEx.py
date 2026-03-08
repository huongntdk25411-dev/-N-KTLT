import csv
import os
import json
from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QColor

from models.user.UserManagerEx import UserManagerEx
from models.user.booking import Booking
from models.user.tabAccount.EditDateEx import EditDateEx
from models.user.tabAccount.feature_change_password.ChangePasswordEx import ChangePasswordEx
from ui.UserMainwindow.MainWindow import Ui_MainWindow


class MainWindowEx(QMainWindow, Ui_MainWindow):

    def __init__(self, user_email=None):
        super().__init__()
        self.setupUi(self)

        self.user_email = user_email
        self.current_user_email = user_email
        self.current_user_data = {}

        self.current_user_bookings = []
        self.selected_row = None

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

        self.json_path = os.path.join(PROJECT_ROOT, "datasets", "bookings.json")
        self.filepath = os.path.join(PROJECT_ROOT, "datasets", "customerin4.csv")

        self.booking = Booking(self)
        self.usermanager = UserManagerEx(self)

        self.tabWidget.setCurrentIndex(0)

        self.setupSignalAndSlot()

        if self.user_email:
            self.load_profile()
            self.load_user_bookings()

        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    # ================= MESSAGE BOX =================

    def create_messagebox(self):

        msg = QMessageBox(self)

        msg.setStyleSheet("""
            QMessageBox {
            background-color: #e8d8c3;
        }

        QLabel {
            color: black;
            font-size: 14px;
        }

        QPushButton {
            color: black;
            background-color: #f5e6d3;
            border: 1px solid #8f8f8f;
            border-radius: 6px;
            padding: 6px 18px;
            min-width: 80px;
        }

        QPushButton:hover {
            background-color: #e0cdb5;
        }
        """)

        return msg

    # ================= SIGNAL =================

    def setupSignalAndSlot(self):

        self.tableWidget.cellClicked.connect(self.show_booking_detail)

        if hasattr(self, "pushButtonChange"):
            self.pushButtonChange.clicked.connect(self.open_edit_window)

        if hasattr(self, "pushButtonDelete"):
            self.pushButtonDelete.clicked.connect(self.delete_booking)

        self.btnUpdate.clicked.connect(self.processUpdate)
        self.btnDeleteAccount.clicked.connect(self.processDeleteAccount)
        self.btnUpdatePass.clicked.connect(self.open_change_password)
        self.btnLogout.clicked.connect(self.logout)

    # ================= TAB =================

    def on_tab_changed(self, index):

        if self.tabWidget.tabText(index) == "Chỉnh lịch":
            self.load_user_bookings()

    # ================= LOAD BOOKING =================

    def load_user_bookings(self):

        if not self.current_user_email:
            return

        try:

            if not os.path.exists(self.json_path):
                return

            with open(self.json_path, "r", encoding="utf-8") as f:
                bookings = json.load(f)

        except Exception as e:
            print("Lỗi đọc JSON:", e)
            return

        user_bookings = [
            b for b in bookings
            if b.get("email", "").strip().lower()
            == self.current_user_email.strip().lower()
        ]

        self.current_user_bookings = user_bookings
        self.display_bookings(user_bookings)

    # ================= DISPLAY BOOKING =================

    def display_bookings(self, bookings):

        self.tableWidget.setRowCount(0)

        now = datetime.now()

        for row_idx, b in enumerate(bookings):

            self.tableWidget.insertRow(row_idx)

            concept = QTableWidgetItem(b.get("concept", ""))
            time = QTableWidgetItem(b.get("time", ""))
            date = QTableWidgetItem(b.get("date", ""))
            place = QTableWidgetItem(b.get("place", ""))

            self.tableWidget.setItem(row_idx, 0, concept)
            self.tableWidget.setItem(row_idx, 1, time)
            self.tableWidget.setItem(row_idx, 2, date)
            self.tableWidget.setItem(row_idx, 3, place)

            try:

                booking_time = datetime.strptime(
                    b.get("date") + " " + b.get("time"),
                    "%d/%m/%Y %H:%M"
                )

                if booking_time < now:
                    color = QColor(255, 200, 200)
                else:
                    color = QColor(200, 255, 200)

                for col in range(4):
                    item = self.tableWidget.item(row_idx, col)
                    if item:
                        item.setBackground(color)

            except:
                pass

    # ================= SHOW DETAIL =================

    def show_booking_detail(self, row, column):

        if row >= len(self.current_user_bookings):
            return

        self.selected_row = row
        data = self.current_user_bookings[row]

        self.lineEditName_2.setText(data.get("name", ""))
        self.lineEditPhone_2.setText(data.get("phone", ""))
        self.lineEditEmail_2.setText(data.get("email", ""))

        self.lineEditConcept.setText(data.get("concept", ""))
        self.lineEditBackground.setText(data.get("background", ""))

        time = data.get("date", "") + " - " + data.get("time", "")
        self.lineEditTime.setText(time)

        place = data.get("place", "")

        if data.get("place_detail"):
            place += " - " + data.get("place_detail")

        self.lineEditPlace.setText(place)

        self.textEditNote.setPlainText(data.get("note", ""))

    # ================= EDIT BOOKING =================

    def open_edit_window(self):

        if self.selected_row is None:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Thông báo")
            msg.setText("Vui lòng chọn lịch cần chỉnh")
            msg.exec()

            return

        data = self.current_user_bookings[self.selected_row]

        self.edit_window = QMainWindow()
        self.edit_ui = EditDateEx()

        self.edit_ui.setupUi(self.edit_window)
        self.edit_ui.load_data(data)

        self.edit_ui.refresh_callback = self.load_user_bookings

        self.edit_window.show()

    # ================= DELETE BOOKING =================

    def delete_booking(self):

        row = self.tableWidget.currentRow()

        if row < 0:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Thông báo")
            msg.setText("Vui lòng chọn lịch cần xóa")
            msg.exec()

            return

        data = self.current_user_bookings[row]

        msg = self.create_messagebox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Xác nhận")
        msg.setText("Bạn có chắc muốn xóa lịch này không?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        reply = msg.exec()

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:

            with open(self.json_path, "r", encoding="utf-8") as f:
                bookings = json.load(f)

            new_bookings = [
                b for b in bookings
                if not (
                        b.get("email") == data.get("email")
                        and b.get("date") == data.get("date")
                        and b.get("time") == data.get("time")
                )
            ]

            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(new_bookings, f, ensure_ascii=False, indent=4)

        except Exception as e:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText(str(e))
            msg.exec()

            return

        msg = self.create_messagebox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thành công")
        msg.setText("Đã xóa lịch")
        msg.exec()

        self.load_user_bookings()

    # ================= UPDATE PROFILE =================

    def processUpdate(self):

        try:

            from models.user.tabAccount.feature_update_info.ui_Account.UpdateProfileDialogEx import UpdateProfileDialogEx

            dlg = UpdateProfileDialogEx(self.user_email)

            result = dlg.exec()

            if result:
                self.load_profile()

        except Exception as e:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText(str(e))
            msg.exec()

    # ================= LOAD PROFILE =================

    def load_profile(self):

        self.current_user_data = {}

        if not os.path.exists(self.filepath):

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Lỗi")
            msg.setText("Không tìm thấy file customerin4.csv")
            msg.exec()

            return

        try:

            with open(self.filepath, "r", encoding="utf-8-sig") as f:

                reader = csv.DictReader(f)

                for row in reader:

                    if row["Email"].strip().lower() == self.user_email.strip().lower():

                        self.current_user_data = row
                        break

        except Exception as e:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi đọc file")
            msg.setText(str(e))
            msg.exec()

            return

        if not self.current_user_data:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Thông báo")
            msg.setText("Không tìm thấy thông tin người dùng")
            msg.exec()

        self.display_profile()

    # ================= DISPLAY PROFILE =================

    def display_profile(self):

        if not self.current_user_data:
            return

        self.lblName.setText(self.current_user_data.get("Họ và tên", ""))
        self.lblEmail.setText(self.current_user_data.get("Email", ""))
        self.lblPhone.setText(self.current_user_data.get("Số điện thoại", ""))
        self.lblDOB.setText(self.current_user_data.get("Ngày sinh", ""))
        self.lblGender.setText(self.current_user_data.get("Giới tính", ""))

    # ================= DELETE ACCOUNT =================

    def processDeleteAccount(self):

        msg = self.create_messagebox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Xác nhận xóa")
        msg.setText("Bạn có chắc chắn muốn xóa tài khoản này không?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        reply = msg.exec()

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:

            with open(self.filepath, "r", encoding="utf-8-sig") as f:

                reader = csv.DictReader(f)
                headers = reader.fieldnames
                users = list(reader)

            new_users = [
                user for user in users
                if user.get("Email", "").strip().lower()
                != self.user_email.strip().lower()
            ]

            with open(self.filepath, "w", encoding="utf-8-sig", newline="") as f:

                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(new_users)

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Thành công")
            msg.setText("Tài khoản đã được xóa!")
            msg.exec()

            self.close()

            from models.login.ui.loginMainWindowEx import LoginMainWindowEx

            self.login_window = LoginMainWindowEx()
            self.login_window.show()

        except Exception as e:

            msg = self.create_messagebox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText(str(e))
            msg.exec()

    # ================= CHANGE PASSWORD =================

    def open_change_password(self):

        self.change_pass_window = ChangePasswordEx(self.user_email)
        self.change_pass_window.show()

    # ================= LOGOUT =================

    def logout(self):

        msg = self.create_messagebox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Đăng xuất")
        msg.setText("Bạn có chắc muốn đăng xuất không?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        reply = msg.exec()

        if reply != QMessageBox.StandardButton.Yes:
            return

        from models.login.ui.loginMainWindowEx import LoginMainWindowEx

        self.login_window = LoginMainWindowEx()
        self.login_window.show()

        self.close()