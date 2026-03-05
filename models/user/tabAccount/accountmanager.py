import csv
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox
from models.user.tabAccount.feature_change_password.ChangePasswordEx import ChangePasswordEx


class AccountManager:
    def __init__(self, main_window, user_email):
        self.mw = main_window
        self.user_email = user_email

        # Tìm thư mục datasets
        current_path = Path(__file__).resolve()
        PROJECT_ROOT = None

        for parent in current_path.parents:
            if (parent / "datasets").exists():
                PROJECT_ROOT = parent
                break

        if PROJECT_ROOT is None:
            raise Exception("Không tìm thấy thư mục datasets")

        self.csv_path = PROJECT_ROOT / "datasets" / "customerin4.csv"

        self.setup_connections()

        # ⭐ KIỂM TRA TAB HIỆN TẠI NGAY KHI MỞ
        self.check_current_tab_on_start()

    # ==============================
    # KẾT NỐI SIGNAL
    # ==============================
    def setup_connections(self):
        self.mw.tabAccount_2.currentChanged.connect(self.check_tab_change)
        self.mw.btnUpdatePass.clicked.connect(self.open_change_password)

    # ==============================
    # KIỂM TRA TAB KHI MỞ CHƯƠNG TRÌNH
    # ==============================
    def check_current_tab_on_start(self):
        current_index = self.mw.tabAccount_2.currentIndex()
        tab_text = self.mw.tabAccount_2.tabText(current_index)

        if "Information" in tab_text or "Thông tin" in tab_text:
            self.load_user_information()

    # ==============================
    # KHI CHUYỂN TAB
    # ==============================
    def check_tab_change(self, index):
        tab_text = self.mw.tabAccount_2.tabText(index)

        if "Information" in tab_text or "Thông tin" in tab_text:
            self.load_user_information()

    # ==============================
    # LOAD THÔNG TIN TỪ CSV
    # ==============================
    def load_user_information(self):
        if not self.csv_path.exists():
            QMessageBox.critical(
                self.mw,
                "Lỗi",
                "Không tìm thấy file customerin4.csv"
            )
            return

        try:
            with open(self.csv_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    if row["Email"].strip().lower() == self.user_email.lower():

                        self.mw.lblName.setText(
                            row.get("Họ và tên", "")
                        )
                        self.mw.lblEmail.setText(
                            row.get("Email", "")
                        )
                        self.mw.lblPhone.setText(
                            row.get("Số điện thoại", "")
                        )

                        return

        except Exception as e:
            QMessageBox.critical(
                self.mw,
                "Lỗi",
                f"Lỗi đọc file: {str(e)}"
            )

    def open_change_password(self):
        self.change_pass_window = ChangePasswordEx(self.user_email)
        self.change_pass_window.show()