import json
import os

from PyQt6.QtWidgets import QWidget, QMessageBox
from USER.Booking.BookingPage import Ui_Form


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "../../../")
)

DATABASE_PATH = os.path.join(
    PROJECT_ROOT,"FINAL_EXAM", "USER", "Booking", "bookings.json"
)


class BookingPageEx(QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.path = DATABASE_PATH
        print("SAVE PATH:", self.path)
        self.setupSignalAndSlot()

        self.loadTimelineByDate()

    # =============================
    # SIGNAL
    # =============================
    def setupSignalAndSlot(self):
        self.pushButtonBook.clicked.connect(self.save_booking)

        self.calendarWidget.selectionChanged.connect(self.syncCalendarToDateEdit)
        self.dateEdit.dateChanged.connect(self.syncDateEditToCalendar)
        self.dateEdit.dateChanged.connect(self.loadTimelineByDate)

    # =============================
    # ĐỒNG BỘ LỊCH
    # =============================
    def syncCalendarToDateEdit(self):
        self.dateEdit.setDate(self.calendarWidget.selectedDate())

    def syncDateEditToCalendar(self):
        self.calendarWidget.setSelectedDate(self.dateEdit.date())

    # =============================
    # LOAD TIMELINE (HIỂN THỊ THEO GIỜ)
    # =============================
    def loadTimelineByDate(self):

        selected_date = self.dateEdit.date().toString("yyyy-MM-dd")
        bookings = self.readData()

        self.listWidgetTimeline.clear()

        # Lọc theo ngày
        day_bookings = [
            b for b in bookings if b.get("date") == selected_date
        ]

        # Sắp xếp theo giờ
        day_bookings.sort(key=lambda x: x.get("time", ""))

        if not day_bookings:
            self.listWidgetTimeline.addItem("Không có lịch đặt trong ngày này.")
            return

        for booking in day_bookings:
            item_text = (
                f"{booking.get('time')} | "
                f"{booking.get('concept')}"
            )
            self.listWidgetTimeline.addItem(item_text)

    # =============================
    # SAVE BOOKING (CÓ GIỜ)
    # =============================
    def save_booking(self):

        name = self.lineEditName.text().strip()
        email = self.lineEditEmail.text().strip()
        phone = self.lineEditPhone.text().strip()
        concept = self.comboBoxConcept.currentText()
        background = self.comboBoxConcept_2.currentText()
        place = self.comboBoxConceptPlace.currentText()
        place_detail = self.lineEditPlace2.text().strip()
        note = self.textEditNote.toPlainText().strip()

        date = self.dateEdit.date().toString("yyyy-MM-dd")

        # 👇 LẤY GIỜ TỪ QTimeEdit
        time = self.timeEdit.time().toString("HH:mm")

        # Service
        if self.radioButtonService1.isChecked():
            service = "Make-up + Làm tóc"
        elif self.radioButtonService1_3.isChecked():
            service = "Khác"
        else:
            service = "Không chọn"

        if name == "" or email == "" or phone == "":
            QMessageBox.warning(
                self,
                "Lỗi",
                "Vui lòng nhập đầy đủ tên, email và số điện thoại!"
            )
            return

        booking = {
            "date": date,
            "time": time,  # 👈 thêm giờ
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

        # ❌ Không cho đặt trùng giờ cùng ngày
        for b in bookings:
            if b.get("date") == date and b.get("time") == time:
                QMessageBox.warning(
                    self,
                    "Trùng giờ",
                    "Khung giờ này đã có người đặt!"
                )
                return

        bookings.append(booking)
        self.writeData(bookings)

        QMessageBox.information(self, "Thông báo", "Đặt lịch thành công!")

        self.loadTimelineByDate()
        self.clearForm()

    # =============================
    # FILE JSON
    # =============================

    def writeData(self, data):
        try:
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("Saved successfully!")

        except Exception as e:
            print("Write file error:", e)

    def readData(self):
        if not os.path.exists(self.path):
            return []

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    # =============================
    # CLEAR FORM
    # =============================
    def clearForm(self):
        self.lineEditName.clear()
        self.lineEditEmail.clear()
        self.lineEditPhone.clear()
        self.lineEditPlace2.clear()
        self.textEditNote.clear()
        self.radioButtonService1.setChecked(False)
        self.radioButtonService1_3.setChecked(False)