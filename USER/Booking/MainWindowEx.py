from PyQt6.QtWidgets import QMainWindow
from USER.Booking import Ui_MainWindow
from Final.timeDateEdit_Customers.Dataset import Dataset
from Final.timeDateEdit_Customers.FileFactory import FileFactory
from Final.timeDateEdit_Customers.models.Booking import Booking


class MainWindowEx(Ui_MainWindow):

    def __init__(self):
        self.MainWindow = None
        self.dataset = Dataset()
        self.fileFactory = FileFactory()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.load_data()
        self.setupSignal()
        self.update_timeline()

    def show(self):
        self.MainWindow.show()

    def load_data(self):
        self.dataset.bookings = self.fileFactory.readData(
            "database.json",
            Booking
        )

    def save_data(self):
        self.fileFactory.writeData(
            "database.json",
            self.dataset.bookings
        )

    def setupSignal(self):
        self.dateTimeEdit.dateTimeChanged.connect(self.on_datetime_changed)
        self.pushButtonBook.clicked.connect(self.book_schedule)

    def on_datetime_changed(self):
        dt = self.dateTimeEdit.dateTime()

        self.lineEditDateTime.setText(
            dt.toString("yyyy-MM-dd HH:mm")
        )

        self.update_timeline()

    def update_timeline(self):
        self.listWidgetTimeline.clear()

        selected_date = self.dateTimeEdit.date()
        bookings = self.dataset.get_bookings_by_date(selected_date)

        if not bookings:
            self.listWidgetTimeline.addItem("Ngày này còn trống")
        else:
            for b in bookings:
                self.listWidgetTimeline.addItem(str(b))

    def book_schedule(self):
        dt = self.dateTimeEdit.dateTime()

        booking = Booking(
            self.lineEditName.text(),
            self.lineEditEmail.text(),
            self.lineEditPhone.text(),
            dt.date(),
            dt.time(),
            self.comboBoxConcept.currentText(),
            self.comboBoxConceptPlace.currentText()
        )

        self.dataset.add(booking)
        self.save_data()
        self.update_timeline()
