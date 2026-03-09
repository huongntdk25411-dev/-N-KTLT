import json
import os
import csv

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView, QHeaderView
)

from ui.AdminMainwindow.AdminMainwindow import Ui_MainWindow
from models.admin.feature_customer_management.ui.EditCustomerDialog import EditCustomerDialog


class AdminMainwindowEx(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.customers_file = os.path.join(BASE_DIR, "datasets", "customerin4.csv")
        self.bookings_file = os.path.join(BASE_DIR, "datasets", "bookings.json")

        self.customers = []
        self.current_email = None
        self.current_booking_row = None

        self.setup_tables()
        self.load_customers()

        # EVENTS
        self.ui.tableWidgetCustomerInfo.cellClicked.connect(self.show_customer_bookings)
        self.ui.tableWidgetDetail.cellClicked.connect(self.select_booking)
        self.ui.tableWidgetDetail.cellDoubleClicked.connect(self.edit_booking)

        self.ui.pushButtonEdit.clicked.connect(self.edit_booking)
        self.ui.pushButtonRemove.clicked.connect(self.delete_booking)

        self.ui.lineEditSearch.textChanged.connect(self.search_customer)

    def setup_tables(self):
        self.ui.tableWidgetCustomerInfo.verticalHeader().setVisible(False)
        self.ui.tableWidgetDetail.verticalHeader().setVisible(False)

        self.ui.tableWidgetCustomerInfo.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableWidgetDetail.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        header_customer = self.ui.tableWidgetCustomerInfo.horizontalHeader()
        header_customer.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        header_detail = self.ui.tableWidgetDetail.horizontalHeader()
        header_detail.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.ui.tableWidgetDetail.setColumnCount(5)
        self.ui.tableWidgetDetail.setHorizontalHeaderLabels(
            ["Concept", "Ngày", "Giờ", "Địa điểm", "Trạng thái"]
        )

    #load customers from csv
    def load_customers(self):
        if not os.path.exists(self.customers_file):
            print("Không tìm thấy khách hàng!")
            return
        self.customers.clear()
        with open(self.customers_file, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                customer = {
                    "name": row["Họ và tên"],
                    "phone": row["Số điện thoại"],
                    "email": row["Email"]
                }
                self.customers.append(customer)
        self.display_customers(self.customers)
        total_customers=self.ui.tableWidgetCustomerInfo.rowCount()
        self.ui.labelTotal.setText(f"Tổng cộng: {total_customers} khách hàng")

    # DISPLAY CUSTOMER TABLE
    def display_customers(self, customer_list):
        table = self.ui.tableWidgetCustomerInfo
        table.setRowCount(0)
        for i, c in enumerate(customer_list):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(c["name"]))
            table.setItem(i, 1, QTableWidgetItem(c["phone"]))
            table.setItem(i, 2, QTableWidgetItem(c["email"]))

    def read_bookings(self):
        if not os.path.exists(self.bookings_file):
            return []
        with open(self.bookings_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    def save_bookings(self, bookings):
        with open(self.bookings_file, "w", encoding="utf-8") as f: json.dump(bookings, f, indent=4, ensure_ascii=False)

    def get_customer_profile(self, email):

        try:
            with open(self.customers_file, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    csv_email = row.get("Email") or row.get("email")
                    if csv_email and csv_email.strip().lower() == email.lower():
                        return {
                            "password": row.get("password") or row.get("Mật khẩu", ""),
                            "phone": row.get("Số điện thoại", ""),
                            "name": row.get("Họ và tên", "")
                        }
        except Exception as e:
            print("Lỗi đọc customer:", e)
        return {}

    # SEARCH CUSTOMER
    def search_customer(self):
        keyword = self.ui.lineEditSearch.text().lower()
        filtered = []
        for c in self.customers:
            if (
                keyword in c["name"].lower()
                or keyword in c["phone"]
                or keyword in c["email"].lower()
            ):
                filtered.append(c)

        self.display_customers(filtered)

    # SHOW BOOKINGS OF CUSTOMER
    def show_customer_bookings(self, row):
        item = self.ui.tableWidgetCustomerInfo.item(row, 2)
        if item is None:
            return
        self.current_email = item.text().strip()
        self.current_booking_row = None
        bookings= self.read_bookings()
        customer_bookings = [
            b for b in bookings
            if b.get("email", "").strip().lower() == self.current_email.lower()
        ]
        # sort theo trạng thái
        status_order = {
            "Đã cọc": 0,
            "Đã xác nhận": 1,
            "Chưa xác nhận": 2,
            "Đã hủy": 3
        }
        customer_bookings.sort(
            key=lambda x: status_order.get(x.get("status", "Chưa xác nhận"), 99)
        )

        table = self.ui.tableWidgetDetail
        table.setRowCount(0)
        if table.columnCount() < 5:
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(["Concept", "Ngày", "Giờ", "Địa điểm", "Trạng thái"])
        for i, b in enumerate(customer_bookings):
            table.insertRow(i)
            concept = b.get("concept", "")
            date = b.get("date", "")
            time = b.get("time", "")
            place = b.get("place", "")
            place_detail = b.get("place_detail", "")
            status = b.get("status", "Chưa xác nhận")
            location = place
            if place_detail: location += " - " + place_detail

            table.setItem(i, 0, QTableWidgetItem(concept))
            table.setItem(i, 1, QTableWidgetItem(date))
            table.setItem(i, 2, QTableWidgetItem(time))
            table.setItem(i, 3, QTableWidgetItem(location))
            status_item = QTableWidgetItem(status)

            if status == "Đã cọc":
                status_item.setBackground(QColor(255, 223, 186))  # cam nhạt
            elif status == "Đã xác nhận":
                status_item.setBackground(QColor(198, 239, 206))  # xanh lá
            elif status == "Chưa xác nhận":
                status_item.setBackground(QColor(255, 242, 204))  # vàng
            elif status == "Đã hủy":
                status_item.setBackground(QColor(255, 199, 206))  # đỏ nhạt

            table.setItem(i, 4, status_item)

    # SELECT BOOKING
    def select_booking(self, row, column):
        self.current_booking_row = row
    # edit booking
    def edit_booking(self, row=None):
        if isinstance(row, int):
            self.current_booking_row = row
        if self.current_email is None:
            QMessageBox.warning(self, "Lỗi", "Chọn khách hàng trước!")
            return
        if self.current_booking_row is None:
            QMessageBox.warning(self, "Lỗi", "Chọn lịch đặt!")
            return
        bookings = self.read_bookings()
        customer_bookings = [
            b for b in bookings
            if b.get("email", "").strip().lower() == self.current_email.lower()
        ]
        if self.current_booking_row >= len(customer_bookings):
            return
        target_booking = customer_bookings[self.current_booking_row]
        # lấy thông tin đăng nhập
        customer_profile = self.get_customer_profile(
            target_booking.get("email")
        )
        # merge booking + profile
        combined_data = {**target_booking, **customer_profile}

        dialog = EditCustomerDialog(combined_data)
        if dialog.exec():
            new_data = dialog.get_data()
            for b in bookings:
                if (
                        b.get("email") == target_booking.get("email")
                        and b.get("date") == target_booking.get("date")
                        and b.get("time") == target_booking.get("time")
                ):
                    b.update(new_data)
                    break

            self.save_bookings(bookings)
            self.show_customer_bookings(
                self.ui.tableWidgetCustomerInfo.currentRow()
            )
            QMessageBox.information(self, "Thành công", "Đã cập nhật lịch đặt!")

    # Delete booking
    def delete_booking(self):
        if self.current_booking_row is None:
            QMessageBox.warning(self,"Cảnh báo","Chưa chọn khách hàng")
            return
        if self.current_booking_row is None:
            QMessageBox.warning(self,"Cảnh báo","Chọn lịch đặt")
            return
        reply=QMessageBox.question(self,"Xác nhận","Bạn có chắc muốn xóa lịch đặt này không?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        bookings=self.read_bookings()
        customer_bookings = [b for b in bookings if b.get("email", "").strip().lower() == self.current_email.lower()]
        if self.current_booking_row >= len(customer_bookings):
            return
        booking=customer_bookings[self.current_booking_row]
        bookings.remove(booking)
        self.save_bookings(bookings)
        self.show_customer_bookings(self.ui.tableWidgetCustomerInfo.currentRow())