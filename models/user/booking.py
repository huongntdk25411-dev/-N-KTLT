import json
import os
import re

from PyQt6.QtGui import QTextCharFormat, QColor, QIntValidator
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, Qt

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
        self.setupCalendar()
        self.markBookingDays()

    def setupSignalAndSlot(self):
        # Kết nối các nút bấm và sự kiện (Dùng self.mw)
        self.mw.pushButtonBook.clicked.connect(self.save_booking)
        self.mw.calendarWidget.selectionChanged.connect(self.syncCalendarToDateEdit)
        self.mw.dateEdit.dateChanged.connect(self.syncDateEditToCalendar)
        self.mw.dateEdit.dateChanged.connect(self.loadTimelineByDate)

        # Auto format name
        self.mw.lineEditName.editingFinished.connect(self.autoCapitalizeName)

        # Email lowercase
        self.mw.lineEditEmail.editingFinished.connect(self.autoLowerEmail)

        # SĐT chỉ có số
        self.mw.lineEditPhone.setValidator(QIntValidator())

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

    #Code bổ sung

    def setupCalendar(self):
        cal = self.mw.calendarWidget

        # Ẩn cột số tuần
        cal.setVerticalHeaderFormat(cal.VerticalHeaderFormat.NoVerticalHeader)

        # Font
        font = cal.font()
        font.setPointSize(10)
        cal.setFont(font)

        # Weekend background
        weekend_format = QTextCharFormat()
        weekend_format.setBackground(QColor("#F5E7D6"))

        cal.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend_format)
        cal.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend_format)

        # Weekday background
        weekday_format = QTextCharFormat()
        weekday_format.setBackground(QColor("#FFF5EB"))

        cal.setWeekdayTextFormat(Qt.DayOfWeek.Monday, weekday_format)
        cal.setWeekdayTextFormat(Qt.DayOfWeek.Tuesday, weekday_format)
        cal.setWeekdayTextFormat(Qt.DayOfWeek.Wednesday, weekday_format)
        cal.setWeekdayTextFormat(Qt.DayOfWeek.Thursday, weekday_format)
        cal.setWeekdayTextFormat(Qt.DayOfWeek.Friday, weekday_format)

        # Today highlight
        today = QDate.currentDate()

        today_format = QTextCharFormat()
        today_format.setBackground(QColor("#FFE4D6"))
        today_format.setForeground(QColor("#000000"))

        cal.setDateTextFormat(today, today_format)

    def markBookingDays(self):
        cal = self.mw.calendarWidget
        bookings = self.readData()

        format_booking = QTextCharFormat()
        format_booking.setForeground(QColor("red"))

        for b in bookings:
            date_str = b.get("date")
            qdate = QDate.fromString(date_str, "dd/MM/yyyy")

            if qdate.isValid():
                format_booking.setToolTip("Có lịch đặt")
                cal.setDateTextFormat(qdate, format_booking)

    def autoCapitalizeName(self): #Cái nì t thêm để nó tự chỉnh nếu chữ cái đầu k viết hoa
        name = self.mw.lineEditName.text().strip()
            # bỏ số nếu có
        name = re.sub(r'\d+', '', name)
            # viết hoa từng chữ
        name = " ".join(word.capitalize() for word in name.split())
        self.mw.lineEditName.setText(name)

    def autoLowerEmail(self):
        email = self.mw.lineEditEmail.text().strip().lower()
        self.mw.lineEditEmail.setText(email)
