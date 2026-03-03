import json
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate

# Đường dẫn database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))
DATABASE_PATH = os.path.join(PROJECT_ROOT, "datasets", "bookings.json")


class Booking:
    def __init__(self, main_window):
        self.mw = main_window  # Lưu lại tham chiếu tới cửa sổ chính
        self.path = DATABASE_PATH
        self.setupSignalAndSlot()
        self.loadTimelineByDate()

    def setupSignalAndSlot(self):
        # Kết nối các nút bấm và sự kiện (Dùng self.mw)
        self.mw.pushButtonBook.clicked.connect(self.save_booking)
        self.mw.calendarWidget.selectionChanged.connect(self.syncCalendarToDateEdit)
        self.mw.dateEdit.dateChanged.connect(self.syncDateEditToCalendar)
        self.mw.dateEdit.dateChanged.connect(self.loadTimelineByDate)

    def syncCalendarToDateEdit(self):
        selected_date = self.mw.calendarWidget.selectedDate()
        self.mw.dateEdit.setDate(selected_date)

    def syncDateEditToCalendar(self):
        selected_date = self.mw.dateEdit.date()
        self.mw.calendarWidget.setSelectedDate(selected_date)

    def loadTimelineByDate(self):
        self.mw.listWidgetTimeline.clear()
        selected_date = self.mw.dateEdit.date().toString("dd/MM/yyyy")
        bookings = self.readData()

        day_bookings = [b for b in bookings if b.get('date') == selected_date]

        if not day_bookings:
            self.mw.listWidgetTimeline.addItem("Không có lịch đặt vào ngày này")
        else:
            day_bookings.sort(key=lambda x: x.get('time'))
            for b in day_bookings:
                item = f"{b.get('time')} | {b.get('concept')} "
                self.mw.listWidgetTimeline.addItem(item)

    def save_booking(self):
        try:
            name = self.mw.lineEditName.text().strip()
            email = self.mw.lineEditEmail.text().strip()
            phone = self.mw.lineEditPhone.text().strip()
            concept = self.mw.comboBoxConcept.currentText()

            background = self.mw.comboBoxConcept_2.currentText() if hasattr(self.mw, 'comboBoxConcept_2') else ""
            place = self.mw.comboBoxConceptPlace.currentText() if hasattr(self.mw, 'comboBoxConceptPlace') else ""
            place_detail = self.mw.lineEditPlace2.text().strip()
            note = self.mw.textEditNote.toPlainText().strip()
            date = self.mw.dateEdit.date().toString("dd/MM/yyyy")
            time = self.mw.timeEdit.time().toString("HH:mm")

            # Xử lý Dịch vụ (RadioButtons)
            service = "Không chọn"
            if self.mw.radioButtonService1.isChecked():
                service = "Make-up + Làm tóc"
            elif self.mw.radioButtonService1_3.isChecked():
                service = "Khác"

            # Kiểm tra nhập liệu
            if not name or not email or not phone:
                QMessageBox.warning(self.mw, "Lỗi", "Vui lòng nhập đầy đủ tên, email và số điện thoại!")
                return

            booking = {
                "date": date,
                "time": time,
                "name": name,
                "email": email,
                "phone": phone,
                "concept": concept,
                "background": background,
                "place": place,
                "place_detail": place_detail,
                "note": note,
                "service": service
            }

            bookings = self.readData()

            # Kiểm tra trùng giờ
            for b in bookings:
                if b.get("date") == date and b.get("time") == time:
                    QMessageBox.warning(self.mw, "Trùng giờ", "Khung giờ này đã có người đặt!")
                    return

            # Lưu dữ liệu
            bookings.append(booking)
            if self.writeData(bookings):
                QMessageBox.information(self.mw, "Thông báo", "Đặt lịch thành công!")
                self.loadTimelineByDate()
                self.clearForm()

        except Exception as e:
            # Bắt lỗi để không bị sập app, hiện lỗi lên màn hình để dễ debug
            QMessageBox.critical(self.mw, "Lỗi hệ thống", f"Phát sinh lỗi khi lưu: {str(e)}")

    def readData(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def writeData(self, data):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Lỗi ghi database: {e}")
            return False

    def clearForm(self):
        self.mw.lineEditName.clear()
        self.mw.lineEditEmail.clear()
        self.mw.lineEditPhone.clear()
        self.mw.lineEditPlace2.clear()
        self.mw.textEditNote.clear()
        self.mw.comboBoxConcept.setCurrentIndex(0)
        if hasattr(self.mw, 'comboBoxPlace'):
            self.mw.comboBoxPlace.setCurrentIndex(0)