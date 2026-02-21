from USER.Booking.CustomerBooking import CustomerBooking
from USER.Booking.FileFactory import FileFactory


class BookingDatabase:

    def __init__(self):
        self.fileFactory = FileFactory()
        self.path = "database.json"
        self.bookings = self.fileFactory.readData(self.path, CustomerBooking)

    def addBooking(self, booking):
        self.bookings.append(booking)
        self.saveData()

    def saveData(self):
        self.fileFactory.writeData(self.path, self.bookings)
