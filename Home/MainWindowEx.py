from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout
from Home.MainWindow import Ui_MainWindow
from USER.Booking.BookingPageEx import BookingPageEx


class MainWindowEx(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ===== TẠO BOOKING PAGE =====
        self.bookingPage = BookingPageEx()

        layout = QVBoxLayout(self.BookingPage)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.bookingPage)

        # ===== MẶC ĐỊNH HIỆN HOME (index 1) =====
        self.stackedWidget.setCurrentIndex(1)

        self.actionBooking=QAction("Đặt lịch", self)
        self.menubar.addAction(self.actionBooking)

        # ===== MENU CLICK =====
        self.actionBooking.triggered.connect(self.openBooking)

    def openBooking(self):
        self.stackedWidget.setCurrentWidget(self.BookingPage)