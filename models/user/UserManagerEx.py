from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from models.user.UserDataService import UserDataService


class UserManagerEx:
    def __init__(self, main_window):
        self.mw = main_window
        self.service = UserDataService()
        self.setupSignalAndSlot()

    def setupSignalAndSlot(self):
        self.mw.btnView_2.clicked.connect(self.handle_search_click)
        self.mw.lineEditSearch_2.returnPressed.connect(self.handle_search_click)

    def handle_search_click(self):
        phone_query = self.mw.lineEditSearch_2.text().strip()

        if not phone_query:
            QMessageBox.warning(self.mw, "Thông báo", "Vui lòng nhập số điện thoại!")
            return

        results = self.service.filter_by_phone(phone_query)

        if not results:
            QMessageBox.information(
                self.mw,
                "Kết quả",
                "Không tìm thấy lịch đặt cho số điện thoại này."
            )
            self.clear_ui()
            return

        self.display_results(results)

    def clear_ui(self):
        self.mw.tableHistory_2.setRowCount(0)
        self.mw.lblName_2.setText("Tên:")
        self.mw.lblPhone_2.setText("SĐT:")
        self.mw.lblEmail_2.setText("Email:")
        self.mw.lblTotalBooking_2.setText("Tìm thấy: 0")

    def display_results(self, results):
        # Hiển thị số lượng
        self.mw.lblTotalBooking_2.setText(
            f"Tìm thấy: {len(results)} lịch hẹn"
        )

        # Đưa vào bảng
        self.mw.tableHistory_2.setRowCount(0)

        for row_idx, b in enumerate(results):
            self.mw.tableHistory_2.insertRow(row_idx)

            self.mw.tableHistory_2.setItem(
                row_idx, 0, QTableWidgetItem(str(row_idx + 1))
            )
            self.mw.tableHistory_2.setItem(
                row_idx, 1, QTableWidgetItem(b.get("date", ""))
            )
            self.mw.tableHistory_2.setItem(
                row_idx, 2, QTableWidgetItem(b.get("time", ""))
            )
            self.mw.tableHistory_2.setItem(
                row_idx, 3, QTableWidgetItem(b.get("concept", ""))
            )
            self.mw.tableHistory_2.setItem(
                row_idx, 4, QTableWidgetItem(b.get("background", ""))
            )
            self.mw.tableHistory_2.setItem(
                row_idx, 5, QTableWidgetItem(b.get("place", ""))
            )
            self.mw.tableHistory_2.setItem(
                row_idx, 6, QTableWidgetItem(b.get("service", ""))
            )

        # Lấy thông tin người dùng từ bản ghi đầu tiên
        first = results[0]

        self.mw.lblName_2.setText(f"Tên: {first.get('name', '')}")
        self.mw.lblPhone_2.setText(f"SĐT: {first.get('phone', '')}")
        self.mw.lblEmail_2.setText(f"Email: {first.get('email', '')}")