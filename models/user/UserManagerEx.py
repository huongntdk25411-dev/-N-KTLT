import csv
import os
import json
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox


class UserManagerEx:

    def __init__(self, mw):
        self.mw = mw

        # =========================
        # PATH
        # =========================
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

        self.csv_path = os.path.join(PROJECT_ROOT, "datasets", "customerin4.csv")
        self.json_path = os.path.join(PROJECT_ROOT, "datasets", "bookings.json")

        # =========================
        # SIGNAL
        # =========================
        self.setupSignalAndSlot()

        # =========================
        # LOAD DATA
        # =========================
        self.load_users()

    # =========================================================
    # SIGNAL
    # =========================================================

    def setupSignalAndSlot(self):

        if hasattr(self.mw, "tableUsers_2"):
            self.mw.tableUsers_2.cellClicked.connect(self.on_user_clicked)

    # =========================================================
    # LOAD USERS
    # =========================================================

    def load_users(self):

        if not hasattr(self.mw, "tableUsers_2"):
            return

        if not os.path.exists(self.csv_path):
            QMessageBox.warning(self.mw, "Lỗi", "Không tìm thấy file customerin4.csv")
            return

        self.mw.tableUsers_2.setRowCount(0)

        try:

            with open(self.csv_path, "r", encoding="utf-8-sig") as f:

                reader = csv.DictReader(f)

                for row_idx, row in enumerate(reader):

                    fullname = row.get("Họ và tên", "")
                    email = row.get("Email", "")

                    self.mw.tableUsers_2.insertRow(row_idx)

                    # STT
                    self.mw.tableUsers_2.setItem(
                        row_idx, 0, QTableWidgetItem(str(row_idx + 1))
                    )

                    # Tên
                    self.mw.tableUsers_2.setItem(
                        row_idx, 1, QTableWidgetItem(fullname)
                    )

                    # Email
                    self.mw.tableUsers_2.setItem(
                        row_idx, 2, QTableWidgetItem(email)
                    )

        except Exception as e:

            QMessageBox.critical(self.mw, "Lỗi đọc file CSV", str(e))

    # =========================================================
    # CLICK USER
    # =========================================================

    def on_user_clicked(self, row, column):

        if not hasattr(self.mw, "tableUsers_2"):
            return

        email_item = self.mw.tableUsers_2.item(row, 2)

        if email_item is None:
            return

        email = email_item.text().strip()

        if not email:
            return

        self.load_user_history(email)

    # =========================================================
    # LOAD USER HISTORY
    # =========================================================

    def load_user_history(self, email):

        if not os.path.exists(self.json_path):
            QMessageBox.warning(self.mw, "Lỗi", "Không tìm thấy file bookings.json")
            return

        try:

            with open(self.json_path, "r", encoding="utf-8") as f:

                try:
                    bookings = json.load(f)
                except json.JSONDecodeError:
                    bookings = []

            user_bookings = [
                b for b in bookings
                if b.get("email", "").strip().lower() == email.lower()
            ]

            self.display_history(user_bookings)

        except Exception as e:

            QMessageBox.critical(self.mw, "Lỗi đọc JSON", str(e))

    # =========================================================
    # DISPLAY HISTORY
    # =========================================================

    def display_history(self, bookings):

        if not hasattr(self.mw, "tableHistory_2"):
            return

        self.mw.tableHistory_2.setRowCount(0)

        for row_idx, b in enumerate(bookings):

            concept = b.get("concept", "")
            date = b.get("date", "")
            time = b.get("time", "")
            place = b.get("place", "")

            self.mw.tableHistory_2.insertRow(row_idx)

            self.mw.tableHistory_2.setItem(
                row_idx, 0, QTableWidgetItem(concept)
            )

            self.mw.tableHistory_2.setItem(
                row_idx, 1, QTableWidgetItem(date)
            )

            self.mw.tableHistory_2.setItem(
                row_idx, 2, QTableWidgetItem(time)
            )

            self.mw.tableHistory_2.setItem(
                row_idx, 3, QTableWidgetItem(place)
            )