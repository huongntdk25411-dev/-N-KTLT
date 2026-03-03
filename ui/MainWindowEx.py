import os
from PyQt6.QtWidgets import QMainWindow

from models.user.UserManagerEx import UserManagerEx
from ui.MainWindow import Ui_MainWindow
from models.user.tabAccount.accountmanager import AccountManager
from models.user.booking import Booking


class MainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, user_email=None):
        super().__init__()
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        # Đường dẫn bookings.json
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
        self.json_path = os.path.join(PROJECT_ROOT, "datasets", "bookings.json")

        self.booking = Booking(self)
        self.usermanager=UserManagerEx(self)

        # Quản lý tài khoản
        if user_email:
            self.account_manager = AccountManager(self, user_email)