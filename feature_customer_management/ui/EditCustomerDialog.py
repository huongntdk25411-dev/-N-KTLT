from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QGroupBox, QHBoxLayout, \
    QPushButton, QMessageBox


class EditCustomerDialog(QDialog):
    def __init__(self,customer,parent=None):
        super().__init__(parent)
        self.customer=customer
        self.setWindowTitle(f"Chỉnh sửa: {customer.name}")
        self.setupUi()
    def setupUi(self):
        main_layout=QVBoxLayout()
        form=QFormLayout()

        #Group 1: thông tin cá nhân cơ bản
        groupboxPersonal=QGroupBox("Thông tin cá nhân cơ bản")
        groupboxPersonal_layout=QFormLayout()

        self.txt_id=QLineEdit(str(self.customer.id))
        self.txt_id.setReadOnly(True) #id mặc định
        self.txt_id.setStyleSheet("background-color: grey;") # tô xám ô ko được chỉnh sửa

        self.txt_name=QLineEdit(self.customer.name)
        self.txt_phone=QLineEdit(self.customer.phone)
        self.txt_email=QLineEdit(self.customer.email)

        groupboxPersonal_layout.addRow("ID:",self.txt_id)
        groupboxPersonal_layout.addRow("Tên Khách hàng:",self.txt_name)
        groupboxPersonal_layout.addRow("Số điện thoại:",self.txt_phone)
        groupboxPersonal_layout.addRow("Email:",self.txt_email)
        groupboxPersonal.setLayout(groupboxPersonal_layout)

        #Group 2: Thông tin đặt lịch (liên kết với module Quản lí lịch)
        groupboxBooking=QGroupBox("Thông tin đặt lịch")
        groupboxBooking_layout=QFormLayout()

        self.txt_concept=QLineEdit(self.customer.concept)
        self.cbo_status = QComboBox()
        self.cbo_status.addItems(["Đã cọc", "Đã xác nhận", "Đã hủy"])
        self.cbo_status.setCurrentText(self.customer.status)

        self.txt_total_fee=QLineEdit(str(self.customer.total_fee))
        self.txt_deposited=QLineEdit(str(self.customer.deposited))
        self.txt_unpaid = QLineEdit(str(self.customer.unpaid()))
        self.txt_unpaid.setReadOnly(True)
        self.txt_unpaid.setStyleSheet("background-color: grey; font-weight: bold;")

        self.txt_location=QLineEdit(self.customer.location)
        self.txt_photographer=QLineEdit(self.customer.photographer)
        self.txt_note=QLineEdit(self.customer.note)

        groupboxBooking_layout.addRow("Gói chụp:",self.txt_concept)
        groupboxBooking_layout.addRow("Trạng thái:",self.cbo_status)
        groupboxBooking_layout.addRow("Tổng chi phí (đ):",self.txt_total_fee)
        groupboxBooking_layout.addRow("Đã đặt cọc (đ):",self.txt_deposited)
        groupboxBooking_layout.addRow("Chưa thanh toán (đ):",self.txt_unpaid)
        groupboxBooking_layout.addRow("Địa điểm chụp:",self.txt_location)
        groupboxBooking_layout.addRow("Thợ chụp:",self.txt_photographer)
        groupboxBooking_layout.addRow("Ghi chú thêm:",self.txt_note)

        groupboxBooking.setLayout(groupboxBooking_layout)

        #tự động tính toán unpaid
        self.txt_total_fee.textChanged.connect(self.update_unpaid)
        self.txt_deposited.textChanged.connect(self.update_unpaid)

        #Group 3: Thông tin hồ sơ hệ thống (Liên kết với module Quản lí hồ sơ khách hàng)
        groupboxProfile=QGroupBox("Thông tin hồ sơ khách hàng trên hệ thống")
        groupboxProfile_layout=QFormLayout()

        self.txt_username=QLineEdit(self.customer.username)
        self.txt_password=QLineEdit(self.customer.password)
        self.txt_last_login=QLineEdit(self.customer.last_login)
        self.txt_username.setReadOnly(True)
        self.txt_password.setReadOnly(True)
        self.txt_last_login.setReadOnly(True)
        self.txt_username.setStyleSheet("background-color: grey;")
        self.txt_password.setStyleSheet("background-color: grey;")
        self.txt_last_login.setStyleSheet("background-color: grey;")

        groupboxProfile_layout.addRow("Tên đăng nhập:",self.txt_username)
        groupboxProfile_layout.addRow("Mật khẩu:",self.txt_password)
        groupboxProfile_layout.addRow("Lần cuối đăng nhập:",self.txt_last_login)
        groupboxProfile.setLayout(groupboxProfile_layout)

        # các nút lệnh
        button_layout=QHBoxLayout()
        self.btn_save=QPushButton("Xác nhận thay đổi")
        self.btn_cancel=QPushButton("Hủy bỏ")
        self.btn_save.setStyleSheet("background-color: blue; color: white; padding: 8px;")
        self.btn_cancel.setStyleSheet("background-color: blue; color: white; padding: 8px;")

        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        main_layout.addWidget(groupboxPersonal)
        main_layout.addWidget(groupboxProfile)
        main_layout.addWidget(groupboxBooking)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        #kết nối sự kiện cho button
        self.btn_save.clicked.connect(self.validate_and_accept)
        self.btn_cancel.clicked.connect(self.reject)

    def validate_and_accept(self):
        try:
            float(self.txt_total_fee.text() or 0)
            float(self.txt_deposited.text() or 0)
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số hợp lệ!")

    def update_unpaid(self):
        # Hàm tự động tính toán tiền Chưa thanh toán khi dữ liệu đầu vào thay đổi
        try:
            total_fee=float(self.txt_total_fee.text() or 0)
            deposited=float(self.txt_deposited.text() or 0)
            unpaid_amount=total_fee - deposited
            self.txt_unpaid.setText(f"{unpaid_amount:,.0f}")
        except ValueError:
            # Nếu người dùng nhập chữ, báo lỗi hoặc để trống
            self.txt_unpaid.setText("Lỗi nhập liệu")

    def get_data(self): # hàm thu thập toàn bộ dữ liệu từ các ô nhập liệu
        return {
            "id":self.txt_id.text(),
            "name": self.txt_name.text(),
            "phone": self.txt_phone.text(),
            "email": self.txt_email.text(),
            "concept": self.txt_concept.text(),
            "status": self.cbo_status.currentText(),
            "total_fee": float(self.txt_total_fee.text() or 0),
            "deposited": float(self.txt_deposited.text() or 0),
            "location": self.txt_location.text(),
            "photographer": self.txt_photographer.text(),
            "note": self.txt_note.text(),
            "username": self.txt_username.text(),
            "password": self.txt_password.text(),
            "last_login": self.txt_last_login.text(),
        }
