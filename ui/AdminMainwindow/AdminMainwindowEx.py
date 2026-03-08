import json
import os
import csv

from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView
)

from ui.AdminMainwindow.AdminMainwindow import Ui_MainWindow
from models.admin.feature_customer_management.ui.EditCustomerDialog import EditCustomerDialog


class AdminMainwindowEx(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # =========================
        # PATH
        # =========================
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.customers_file = os.path.join(BASE_DIR, "datasets", "customerin4.csv")
        self.bookings_file = os.path.join(BASE_DIR, "datasets", "bookings.json")

        # =========================
        # VARIABLES
        # =========================
        self.customers = []
        self.current_email = None
        self.current_booking_row = None

        # =========================
        # TABLE SETTINGS
        # =========================
        self.ui.tableWidgetCustomerInfo.verticalHeader().setVisible(False)
        self.ui.tableWidgetDetail.verticalHeader().setVisible(False)

        self.ui.tableWidgetCustomerInfo.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.ui.tableWidgetDetail.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        # =========================
        # LOAD DATA
        # =========================
        self.load_customers()

        # =========================
        # EVENTS
        # =========================
        self.ui.tableWidgetCustomerInfo.cellClicked.connect(
            self.show_customer_bookings
        )

        self.ui.tableWidgetDetail.cellClicked.connect(
            self.select_booking
        )

        self.ui.tableWidgetDetail.cellDoubleClicked.connect(
            self.edit_booking
        )

        self.ui.pushButtonEdit.clicked.connect(self.edit_booking)
        self.ui.pushButtonRemove.clicked.connect(self.delete_booking)

        self.ui.lineEditSearch.textChanged.connect(self.search_customer)

    # ==========================================
    # LOAD CUSTOMERS FROM CSV
    # ==========================================
    def load_customers(self):

        if not os.path.exists(self.customers_file):
            print("Customer file NOT found")
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


    # ==========================================
    # DISPLAY CUSTOMER TABLE
    # ==========================================
    def display_customers(self, customer_list):

        table = self.ui.tableWidgetCustomerInfo
        table.setRowCount(0)

        for i, c in enumerate(customer_list):

            table.insertRow(i)

            table.setItem(i, 0, QTableWidgetItem(c["name"]))
            table.setItem(i, 1, QTableWidgetItem(c["phone"]))
            table.setItem(i, 2, QTableWidgetItem(c["email"]))

    # ==========================================
    # SEARCH CUSTOMER
    # ==========================================
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

    # ==========================================
    # SHOW BOOKINGS OF CUSTOMER
    # ==========================================
    def show_customer_bookings(self, row, column):

        item = self.ui.tableWidgetCustomerInfo.item(row, 2)

        if item is None:
            return

        self.current_email = item.text().strip()
        self.current_booking_row = None

        if not os.path.exists(self.bookings_file):
            return

        with open(self.bookings_file, "r", encoding="utf-8") as f:
            bookings = json.load(f)

        customer_bookings = [
            b for b in bookings
            if b.get("email", "").strip().lower()
            == self.current_email.lower()
        ]

        table = self.ui.tableWidgetDetail
        table.setRowCount(0)

        for i, b in enumerate(customer_bookings):

            table.insertRow(i)

            concept = b.get("concept", "")
            date = b.get("date", "")
            time = b.get("time", "")

            place = b.get("place", "")
            place_detail = b.get("place_detail", "")

            location = place
            if place_detail:
                location = place + " - " + place_detail

            table.setItem(i, 0, QTableWidgetItem(concept))
            table.setItem(i, 1, QTableWidgetItem(date))
            table.setItem(i, 2, QTableWidgetItem(time))
            table.setItem(i, 3, QTableWidgetItem(location))

    # ==========================================
    # SELECT BOOKING
    # ==========================================
    def select_booking(self, row, column):

        self.current_booking_row = row

    # ==========================================
    # EDIT BOOKING
    # ==========================================
    def edit_booking(self, row=None, column=None):

        if row is not None:
            self.current_booking_row = row

        if self.current_email is None:
            QMessageBox.warning(self, "Warning", "Please select a customer")
            return

        if self.current_booking_row is None:
            QMessageBox.warning(self, "Warning", "Please select a booking")
            return

        with open(self.bookings_file, "r", encoding="utf-8") as f:
            bookings = json.load(f)

        customer_bookings = [
            b for b in bookings if b.get("email") == self.current_email
        ]

        if self.current_booking_row >= len(customer_bookings):
            return

        booking = customer_bookings[self.current_booking_row]

        dialog = EditCustomerDialog(booking)

        if dialog.exec():

            new_data = dialog.get_data()

            booking.update(new_data)

            with open(self.bookings_file, "w", encoding="utf-8") as f:
                json.dump(bookings, f, indent=4, ensure_ascii=False)

            self.show_customer_bookings(
                self.ui.tableWidgetCustomerInfo.currentRow(), 0
            )

    # ==========================================
    # DELETE BOOKING
    # ==========================================
    def delete_booking(self):

        if self.current_email is None:
            QMessageBox.warning(self, "Warning", "Select customer first")
            return

        if self.current_booking_row is None:
            QMessageBox.warning(self, "Warning", "Select booking first")
            return

        reply = QMessageBox.question(
            self,
            "Confirm",
            "Delete this booking?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        with open(self.bookings_file, "r", encoding="utf-8") as f:
            bookings = json.load(f)

        customer_bookings = [
            b for b in bookings if b.get("email") == self.current_email
        ]

        if self.current_booking_row >= len(customer_bookings):
            return

        booking = customer_bookings[self.current_booking_row]

        bookings.remove(booking)

        with open(self.bookings_file, "w", encoding="utf-8") as f:
            json.dump(bookings, f, indent=4, ensure_ascii=False)

        self.show_customer_bookings(
            self.ui.tableWidgetCustomerInfo.currentRow(), 0
        )