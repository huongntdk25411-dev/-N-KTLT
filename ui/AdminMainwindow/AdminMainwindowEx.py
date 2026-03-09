import csv
import json
import os

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QHeaderView
)

from PyQt6.QtCore import Qt

from models.admin.feature_customer_management.ui.UserDetailDialog import UserDetailDialog
from models.admin.feature_customer_management.ui.EditCustomerDialog import EditCustomerDialog
from ui.AdminMainwindow.AdminMainwindow import Ui_MainWindow


class AdminMainwindowEx(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.users_file = os.path.join(BASE_DIR, "datasets", "customerin4.csv")
        self.bookings_file = os.path.join(BASE_DIR, "datasets", "bookings.json")

        self.users = []
        self.customers = []

        self.current_email = None
        self.current_booking_row = None

        # setup tables
        self.setup_tables()

        # load data
        self.load_users()
        self.load_customers()

        # EVENTS TAB 1
        self.ui.tableUsers.cellClicked.connect(self.show_user_history)
        self.ui.btnView.clicked.connect(self.view_user)
        self.ui.btnDeleteUser.clicked.connect(self.delete_user)
        self.ui.lineEditSearch_2.textChanged.connect(self.search_user)

        # EVENTS TAB 2
        self.ui.tableWidgetCustomerInfo.cellClicked.connect(self.show_customer_bookings)
        self.ui.tableWidgetDetail.cellClicked.connect(self.select_booking)
        self.ui.tableWidgetDetail.cellDoubleClicked.connect(self.edit_booking)

        self.ui.pushButtonEdit.clicked.connect(self.edit_booking)
        self.ui.pushButtonRemove.clicked.connect(self.delete_booking)
        self.ui.lineEditSearch.textChanged.connect(self.search_customer)

    # ================= TABLE SETTINGS =================

    def setup_tables(self):

        # TAB hồ sơ
        self.ui.tableUsers.verticalHeader().setVisible(False)
        self.ui.tableUsers.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # TAB khách hàng
        self.ui.tableWidgetCustomerInfo.verticalHeader().setVisible(False)
        self.ui.tableWidgetDetail.verticalHeader().setVisible(False)

        self.ui.tableWidgetCustomerInfo.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableWidgetDetail.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        header = self.ui.tableWidgetDetail.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # ================= LOAD USERS (TAB 1) =================

    def load_users(self):

        if not os.path.exists(self.users_file):
            print("Không tìm thấy file:", self.users_file)
            return

        self.users = []

        with open(self.users_file, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)
            reader.fieldnames = [field.strip() for field in reader.fieldnames]

            for row in reader:

                clean_row = {}
                for key, value in row.items():
                    clean_row[key.strip()] = value.strip() if value else ""

                if "Trạng thái" not in clean_row:
                    clean_row["Trạng thái"] = "Hoạt động"

                self.users.append(clean_row)

        self.display_users(self.users)

    # ================= DISPLAY USERS =================

    def display_users(self, user_list):

        table = self.ui.tableUsers
        table.setRowCount(len(user_list))

        for row, user in enumerate(user_list):
            stt = QTableWidgetItem(str(row + 1))
            stt.setFlags(stt.flags() & ~Qt.ItemFlag.ItemIsEditable)

            table.setItem(row, 0, stt)
            table.setItem(row, 1, QTableWidgetItem(user.get("Họ và tên", "")))
            table.setItem(row, 2, QTableWidgetItem(user.get("Email", "")))
            table.setItem(row, 3, QTableWidgetItem(user.get("Số điện thoại", "")))
            table.setItem(row, 4, QTableWidgetItem(user.get("Trạng thái", "Hoạt động")))

        table.resizeColumnsToContents()

    # ================= SEARCH USER =================

    def search_user(self):

        keyword = self.ui.lineEditSearch_2.text().lower()

        filtered = [
            u for u in self.users
            if keyword in u.get("Họ và tên", "").lower()
               or keyword in u.get("Email", "").lower()
               or keyword in u.get("Số điện thoại", "").lower()
        ]

        self.display_users(filtered)

    # ================= READ BOOKINGS =================

    def read_bookings(self):

        if not os.path.exists(self.bookings_file):
            return []

        with open(self.bookings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # ================= SHOW USER INFO =================

    def show_user_history(self, row, column):

        name = self.ui.tableUsers.item(row, 1).text()
        email = self.ui.tableUsers.item(row, 2).text()
        phone = self.ui.tableUsers.item(row, 3).text()
        status = self.ui.tableUsers.item(row, 4).text()

        self.ui.lblName.setText(f"Tên: {name}")
        self.ui.lblEmail.setText(f"Email: {email}")
        self.ui.lblPhone.setText(f"SĐT: {phone}")
        self.ui.lblStatus.setText(f"Trạng thái: {status}")

        self.load_history(email)

    # ================= LOAD HISTORY =================

    def load_history(self, email):

        bookings = self.read_bookings()

        user_bookings = [
            b for b in bookings
            if b.get("email", "").strip().lower() == email.lower()
        ]

        table = self.ui.tableHistory
        table.setRowCount(0)

        for row, b in enumerate(user_bookings):

            table.insertRow(row)

            stt = QTableWidgetItem(str(row + 1))
            concept = QTableWidgetItem(b.get("concept", ""))
            date = QTableWidgetItem(b.get("date", ""))
            time = QTableWidgetItem(b.get("time", ""))

            place = b.get("place", "")
            place_detail = b.get("place_detail", "")

            if place_detail:
                place = place + " - " + place_detail

            table.setItem(row, 0, stt)
            table.setItem(row, 1, concept)
            table.setItem(row, 2, date)
            table.setItem(row, 3, time)
            table.setItem(row, 4, QTableWidgetItem(place))

        table.resizeColumnsToContents()

        self.ui.lblTotalBooking.setText(
            f"Tổng số lần đặt lịch: {len(user_bookings)}"
        )

    # ================= VIEW USER =================

    def view_user(self):

        row = self.ui.tableUsers.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Warning", "Chọn user trước")
            return

        email = self.ui.tableUsers.item(row, 2).text()

        user = None

        for u in self.users:
            if u.get("Email", "").lower() == email.lower():
                user = u
                break

        if user is None:
            QMessageBox.warning(self, "Warning", "Không tìm thấy user")
            return

        dialog = UserDetailDialog(user)

        if dialog.exec():
            self.load_users()

    # ================= DELETE USER =================

    def delete_user(self):

        row = self.ui.tableUsers.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Warning", "Chọn user trước")
            return

        confirm = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn xóa user này?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.No:
            return

        email = self.ui.tableUsers.item(row, 2).text()

        self.users = [u for u in self.users if u.get("Email") != email]

        self.save_users()

        self.load_users()

        QMessageBox.information(self, "Thông báo", "Đã xóa user")

    # ================= SAVE USERS =================

    def save_users(self):

        fieldnames = [
            "Họ và tên",
            "Email",
            "Số điện thoại",
            "Ngày sinh",
            "Giới tính",
            "Mật khẩu",
            "Trạng thái"
        ]

        with open(self.users_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for user in self.users:
                writer.writerow(user)

    # ================= TAB 2 =================

    def load_customers(self):

        if not os.path.exists(self.users_file):
            return

        self.customers.clear()

        with open(self.users_file,newline="",encoding="utf-8-sig") as f:

            reader=csv.DictReader(f)

            for row in reader:

                self.customers.append({
                    "name":row.get("Họ và tên",""),
                    "phone":row.get("Số điện thoại",""),
                    "email":row.get("Email","")
                })

        self.display_customers(self.customers)

    def display_customers(self,customers):

        table=self.ui.tableWidgetCustomerInfo
        table.setRowCount(0)

        for i,c in enumerate(customers):

            table.insertRow(i)

            table.setItem(i,0,QTableWidgetItem(c["name"]))
            table.setItem(i,1,QTableWidgetItem(c["phone"]))
            table.setItem(i,2,QTableWidgetItem(c["email"]))

    # ================= BOOKING =================

    def read_bookings(self):

        if not os.path.exists(self.bookings_file):
            return []

        with open(self.bookings_file,"r",encoding="utf-8") as f:
            return json.load(f)

    def show_customer_bookings(self,row):

        email=self.ui.tableWidgetCustomerInfo.item(row,2).text()

        self.current_email=email

        bookings=self.read_bookings()

        customer_bookings=[b for b in bookings if b.get("email","")==email]

        table=self.ui.tableWidgetDetail
        table.setRowCount(0)

        for i,b in enumerate(customer_bookings):

            table.insertRow(i)

            table.setItem(i,0,QTableWidgetItem(b.get("concept","")))
            table.setItem(i,1,QTableWidgetItem(b.get("date","")))
            table.setItem(i,2,QTableWidgetItem(b.get("time","")))
            table.setItem(i,3,QTableWidgetItem(b.get("place","")))

            status=b.get("status","Chưa xác nhận")

            status_item=QTableWidgetItem(status)

            if status=="Đã cọc":
                status_item.setBackground(QColor(255,223,186))

            elif status=="Đã xác nhận":
                status_item.setBackground(QColor(198,239,206))

            elif status=="Chưa xác nhận":
                status_item.setBackground(QColor(255,242,204))

            elif status=="Đã hủy":
                status_item.setBackground(QColor(255,199,206))

            table.setItem(i,4,status_item)

    # ================= SELECT BOOKING =================

    def select_booking(self,row,column):

        self.current_booking_row=row

    # ================= EDIT BOOKING =================

    def edit_booking(self):

        if self.current_booking_row is None:
            return

        bookings=self.read_bookings()

        customer_bookings=[b for b in bookings if b.get("email","")==self.current_email]

        booking=customer_bookings[self.current_booking_row]

        dialog=EditCustomerDialog(booking)

        if dialog.exec():

            booking.update(dialog.get_data())

            with open(self.bookings_file,"w",encoding="utf-8") as f:
                json.dump(bookings,f,indent=4,ensure_ascii=False)

            self.show_customer_bookings(
                self.ui.tableWidgetCustomerInfo.currentRow()
            )

    # ================= DELETE BOOKING =================

    def delete_booking(self):

        if self.current_booking_row is None:
            return

        bookings=self.read_bookings()

        customer_bookings=[b for b in bookings if b.get("email","")==self.current_email]

        booking=customer_bookings[self.current_booking_row]

        bookings.remove(booking)

        with open(self.bookings_file,"w",encoding="utf-8") as f:
            json.dump(bookings,f,indent=4,ensure_ascii=False)

        self.show_customer_bookings(
            self.ui.tableWidgetCustomerInfo.currentRow()
        )

    # ================= SEARCH CUSTOMER =================

    def search_customer(self):

        keyword=self.ui.lineEditSearch.text().lower()

        filtered=[
            c for c in self.customers
            if keyword in c["name"].lower()
            or keyword in c["phone"]
            or keyword in c["email"].lower()
        ]

        self.display_customers(filtered)
