from Final.timeDateEdit_Customers.FileFactory import FileFactory
from Final.timeDateEdit_Customers.models.Booking import Booking
ff=FileFactory()
ff.readData("../dataset/database.json", Booking)