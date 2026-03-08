from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QGroupBox, QHBoxLayout,
    QPushButton, QMessageBox
)


class EditCustomerDialog(QDialog):
    def __init__(self, customer, parent=None):
        super().__init__(parent)

        # customer thực tế là dict
        self.customer = customer

        name = customer.get("name", "")
        self.setWindowTitle(f"Chỉnh sửa: {name}")

        self.setupUi()

    def setupUi(self):

        main_layout = QVBoxLayout()

        # =========================
        # Group 1: Thông tin cá nhân
        # =========================
        groupboxPersonal = QGroupBox("Thông tin cá nhân cơ bản")
        groupboxPersonal_layout = QFormLayout()

        customer_id = self.customer.get("id", self.customer.get("email", ""))

        self.txt_id = QLineEdit(str(customer_id))
        self.txt_id.setReadOnly(True)
        self.txt_id.setStyleSheet("background-color: lightgray;")

        self.txt_name = QLineEdit(self.customer.get("name", ""))
        self.txt_phone = QLineEdit(self.customer.get("phone", ""))
        self.txt_email = QLineEdit(self.customer.get("email", ""))

        groupboxPersonal_layout.addRow("ID:", self.txt_id)
        groupboxPersonal_layout.addRow("Tên Khách hàng:", self.txt_name)
        groupboxPersonal_layout.addRow("Số điện thoại:", self.txt_phone)
        groupboxPersonal_layout.addRow("Email:", self.txt_email)

        groupboxPersonal.setLayout(groupboxPersonal_layout)

        # =========================
        # Group 2: Thông tin đặt lịch
        # =========================
        groupboxBooking = QGroupBox("Thông tin đặt lịch")
        groupboxBooking_layout = QFormLayout()

        self.txt_concept = QLineEdit(self.customer.get("concept", ""))

        self.cbo_status = QComboBox()
        self.cbo_status.addItems(["Đã cọc", "Đã xác nhận", "Đã hủy"])
        self.cbo_status.setCurrentText(self.customer.get("status", "Đã xác nhận"))

        self.txt_total_fee = QLineEdit(str(self.customer.get("total_fee", 0)))
        self.txt_deposited = QLineEdit(str(self.customer.get("deposited", 0)))

        unpaid = float(self.customer.get("total_fee", 0)) - float(self.customer.get("deposited", 0))

        self.txt_unpaid = QLineEdit(str(unpaid))
        self.txt_unpaid.setReadOnly(True)
        self.txt_unpaid.setStyleSheet("background-color: lightgray; font-weight: bold;")

        self.txt_location = QLineEdit(self.customer.get("place"+"place_detail", ""))
        self.txt_photographer = QLineEdit(self.customer.get("photographer", ""))
        self.txt_note = QLineEdit(self.customer.get("note", ""))

        groupboxBooking_layout.addRow("Gói chụp:", self.txt_concept)
        groupboxBooking_layout.addRow("Trạng thái:", self.cbo_status)
        groupboxBooking_layout.addRow("Tổng chi phí (đ):", self.txt_total_fee)
        groupboxBooking_layout.addRow("Đã đặt cọc (đ):", self.txt_deposited)
        groupboxBooking_layout.addRow("Chưa thanh toán (đ):", self.txt_unpaid)
        groupboxBooking_layout.addRow("Địa điểm chụp:", self.txt_location)
        groupboxBooking_layout.addRow("Thợ chụp:", self.txt_photographer)
        groupboxBooking_layout.addRow("Ghi chú thêm:", self.txt_note)

        groupboxBooking.setLayout(groupboxBooking_layout)

        # tự động tính unpaid
        self.txt_total_fee.textChanged.connect(self.update_unpaid)
        self.txt_deposited.textChanged.connect(self.update_unpaid)

        # =========================
        # Group 3: Thông tin hệ thống
        # =========================
        groupboxProfile = QGroupBox("Thông tin hồ sơ khách hàng trên hệ thống")
        groupboxProfile_layout = QFormLayout()

        self.txt_username = QLineEdit(self.customer.get("Email", ""))
        self.txt_password = QLineEdit(self.customer.get("password", ""))
        self.txt_last_login = QLineEdit(str(self.customer.get("last_login", "")))

        self.txt_username.setReadOnly(True)
        self.txt_password.setReadOnly(True)
        self.txt_last_login.setReadOnly(True)

        self.txt_username.setStyleSheet("background-color: lightgray;")
        self.txt_password.setStyleSheet("background-color: lightgray;")
        self.txt_last_login.setStyleSheet("background-color: lightgray;")

        groupboxProfile_layout.addRow("Tên đăng nhập:", self.txt_username)
        groupboxProfile_layout.addRow("Mật khẩu:", self.txt_password)
        groupboxProfile_layout.addRow("Lần cuối đăng nhập:", self.txt_last_login)

        groupboxProfile.setLayout(groupboxProfile_layout)

        # =========================
        # Buttons
        # =========================
        button_layout = QHBoxLayout()

        self.btn_save = QPushButton("Xác nhận thay đổi")
        self.btn_cancel = QPushButton("Hủy bỏ")

        self.btn_save.setStyleSheet("background-color: blue; color: white; padding: 8px;")
        self.btn_cancel.setStyleSheet("background-color: blue; color: white; padding: 8px;")

        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        # =========================
        # Layout tổng
        # =========================
        main_layout.addWidget(groupboxPersonal)
        main_layout.addWidget(groupboxBooking)
        main_layout.addWidget(groupboxProfile)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Events
        self.btn_save.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

    # =========================
    # Kiểm tra dữ liệu
    # =========================
    def validate_and_accept(self):
        try:
            float(self.txt_total_fee.text().replace(",", "") or 0)
            float(self.txt_deposited.text().replace(",", "") or 0)
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số hợp lệ!")

    # =========================
    # Tự động tính unpaid
    # =========================
    def update_unpaid(self):
        try:
            total_fee = float(self.txt_total_fee.text().replace(",", "") or 0)
            deposited = float(self.txt_deposited.text().replace(",", "") or 0)

            unpaid_amount = total_fee - deposited

            self.txt_unpaid.setText(f"{unpaid_amount:,.0f}")

        except ValueError:
            self.txt_unpaid.setText("Lỗi nhập liệu")

    # =========================
    # Lấy dữ liệu sau khi sửa
    # =========================
    def get_data(self):

        total = float(self.txt_total_fee.text().replace(",", "") or 0)
        deposited = float(self.txt_deposited.text().replace(",", "") or 0)

        return {
            "name": self.txt_name.text(),
            "phone": self.txt_phone.text(),
            "email": self.txt_email.text(),
            "concept": self.txt_concept.text(),
            "status": self.cbo_status.currentText(),
            "total_fee": total,
            "deposited": deposited,
            "location": self.txt_location.text(),
            "photographer": self.txt_photographer.text(),
            "note": self.txt_note.text(),
            "username": self.txt_username.text(),
            "password": self.txt_password.text(),
            "last_login": self.txt_last_login.text(),
        }