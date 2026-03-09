from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QGroupBox, QHBoxLayout,
                             QPushButton, QMessageBox, QPlainTextEdit, QCheckBox)

class EditCustomerDialog(QDialog):
    def __init__(self, customer, parent=None):
        super().__init__(parent)
        # customer truyền vào từ file json là 1 dictionary
        self.customer=customer if isinstance(customer,dict) else {}

        name=self.customer.get("name","")
        self.setWindowTitle(f"Chỉnh sửa: {name}")
        self.resize(900, 700)
        self.setMinimumSize(850, 650)

        self.setupUi()
        self.apply_style() #giao dien

    def setupUi(self):
        main_layout = QVBoxLayout()
        columns_layout = QHBoxLayout()

        left_column = QVBoxLayout()
        right_column = QVBoxLayout()
        # Group 1: Thông tin cá nhân
        groupboxPersonal = QGroupBox("Thông tin cá nhân cơ bản")
        groupboxPersonal_layout = QFormLayout()

        self.txt_email = QLineEdit(self.customer.get("email", ""))
        self.txt_email.setReadOnly(True)

        self.txt_name = QLineEdit(self.customer.get("name", ""))
        self.txt_phone = QLineEdit(self.customer.get("phone", ""))

        groupboxPersonal_layout.addRow("Tên Khách hàng:", self.txt_name)
        groupboxPersonal_layout.addRow("Số điện thoại:", self.txt_phone)
        groupboxPersonal_layout.addRow("Email liên hệ:", self.txt_email)

        groupboxPersonal.setLayout(groupboxPersonal_layout)

        # Group 2: Thông tin gói chụp
        groupboxSelectedService = QGroupBox("Thông tin gói chụp")
        groupboxSelectedService_layout = QFormLayout()

        self.txt_concept = QLineEdit(self.customer.get("concept", ""))

        self.cbo_status = QComboBox()
        self.cbo_status.addItems(["Đã cọc", "Đã xác nhận", "Đã hủy"])
        self.cbo_status.setCurrentText(self.customer.get("status","Chưa xác nhận"))

        self.txt_background=QLineEdit(self.customer.get("background", ""))
        self.txt_place=QLineEdit(self.customer.get("place", ""))
        self.txt_place_detail=QLineEdit(self.customer.get("place_detail", ""))
        self.txt_note=QPlainTextEdit(self.customer.get("note", ""))
        self.txt_service=QLineEdit(self.customer.get("service", ""))

        if self.txt_place_detail.text().strip() == "":
            self.txt_place_detail.setText("New Year Photo Studio")

        groupboxSelectedService_layout.addRow("Gói chụp:", self.txt_concept)
        groupboxSelectedService_layout.addRow("Trạng thái:", self.cbo_status)
        groupboxSelectedService_layout.addRow("Bối cảnh:",self.txt_background)
        groupboxSelectedService_layout.addRow("Khu vực:", self.txt_place)
        groupboxSelectedService_layout.addRow("Địa chỉ:",self.txt_place_detail)
        groupboxSelectedService_layout.addRow("Dịch vụ khác:",self.txt_service)
        groupboxSelectedService_layout.addRow("Ghi chú thêm:", self.txt_note)

        groupboxSelectedService.setLayout(groupboxSelectedService_layout)

        # Group 3: Thông tin lịch đặt
        groupboxBooking = QGroupBox("Thông tin lịch đặt")
        groupboxBooking_layout = QFormLayout()

        self.txt_date=QLineEdit(self.customer.get("date", ""))
        self.txt_time=QLineEdit(self.customer.get("time", ""))
        # Lấy giá trị tiền, nếu không có trong file bookings.json thì mặc định là 0
        total_fee = self.customer.get("total_fee", 0)
        deposited = self.customer.get("deposited", 0)

        self.txt_total_fee = QLineEdit(str(total_fee))
        self.txt_deposited = QLineEdit(str(deposited))

        # Tự động tính unpaid ban đầu
        self.txt_unpaid = QLineEdit(str(float(total_fee) - float(deposited)))
        self.txt_unpaid.setReadOnly(True)
        # tự động tính unpaid khi thay đổi tiền cọc
        self.txt_total_fee.textChanged.connect(self.update_unpaid)
        self.txt_deposited.textChanged.connect(self.update_unpaid)
        self.txt_photographer = QLineEdit(self.customer.get("photographer", ""))

        groupboxBooking_layout.addRow("Ngày chụp:",self.txt_date)
        groupboxBooking_layout.addRow("Thời gian:",self.txt_time)
        groupboxBooking_layout.addRow("Tổng chi phí (đ):", self.txt_total_fee)
        groupboxBooking_layout.addRow("Đã đặt cọc (đ):", self.txt_deposited)
        groupboxBooking_layout.addRow("Chưa thanh toán (đ):", self.txt_unpaid)
        groupboxBooking_layout.addRow("Thợ chụp:",self.txt_photographer)

        groupboxBooking.setLayout(groupboxBooking_layout)

        # Group 4: Thông tin hệ thống
        groupboxProfile = QGroupBox("Thông tin hồ sơ khách hàng trên hệ thống")
        groupboxProfile_layout = QFormLayout()

        self.txt_login_email = QLineEdit(self.customer.get("email", ""))
        self.txt_login_email.setReadOnly(True)
        self.txt_password = QLineEdit(self.customer.get("password", ""))
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setReadOnly(True)

        self.chk_show_pass = QCheckBox("Hiển thị mật khẩu")
        self.chk_show_pass.stateChanged.connect(self.toggle_password)

        pass_layout = QVBoxLayout()
        pass_layout.addWidget(self.txt_password)
        pass_layout.addWidget(self.chk_show_pass)

        groupboxProfile_layout.addRow("Email đăng nhập:", self.txt_login_email)
        groupboxProfile_layout.addRow("Mật khẩu:", pass_layout)

        groupboxProfile.setLayout(groupboxProfile_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight) # đẩy 2 button sang phải

        self.btn_save = QPushButton("Xác nhận thay đổi")
        self.btn_cancel = QPushButton("Hủy bỏ")
        self.btn_save.setObjectName("btn_save")
        self.btn_cancel.setObjectName("btn_cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)

        # cột trái
        left_column.addWidget(groupboxSelectedService)
        left_column.addWidget(groupboxBooking)
        # cột phải
        right_column.addWidget(groupboxPersonal)
        right_column.addWidget(groupboxProfile)
        # ghép 2 cột
        columns_layout.addLayout(left_column)
        columns_layout.addLayout(right_column)
        # layout tổng
        main_layout.addLayout(columns_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Events
        self.btn_save.clicked.connect(self.processSave)
        self.btn_cancel.clicked.connect(self.processCancel)

    def toggle_password(self, state):
        if state:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

    # Kiểm tra dữ liệu
    def processSave(self):
        #1. kiểm tra dữ liệu nhập mới có hợp lệ ko
        try:
            float(self.txt_total_fee.text().replace(",", "") or 0)
            float(self.txt_deposited.text().replace(",", "") or 0)
        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Chi phí và tiền cọc phải là số hợp lệ!")
            return
        #2. Nếu dữ liệu hợp lệ -> hỏi xác nhận
        name = self.customer.get("name", "")
        reply=QMessageBox.question(self,"Xác nhận thay đổi",f"Bạn có chắc chắn muốn cập nhật thông tin khách hàng {name} không?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)
        # mặc định ko
        # 3.Nếu chọn Yes -> đóng cửa sổ dialog và thông báo thành công
        if reply == QMessageBox.StandardButton.Yes:
            self.accept()

    def processCancel(self):
        reply=QMessageBox.question(self,"Xác nhận hủy",f"Bạn có chắc muốn hủy bỏ thay đổi không?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.reject()

    # Tự động tính unpaid
    def update_unpaid(self):
        try:
            total_fee = float(self.txt_total_fee.text().replace(",", "") or 0)
            deposited = float(self.txt_deposited.text().replace(",", "") or 0)
            unpaid_amount = total_fee - deposited
            self.txt_unpaid.setText(f"{unpaid_amount:,.0f}")
        except ValueError:
            self.txt_unpaid.setText("Lỗi nhập liệu")

    # Lấy dữ liệu sau khi sửa
    def get_data(self):
        return {
            "name": self.txt_name.text(),
            "phone": self.txt_phone.text(),
            "email": self.txt_email.text(),
            "concept": self.txt_concept.text(),
            "status": self.cbo_status.currentText(),
            "total_fee": float(self.txt_total_fee.text().replace(",", "") or 0),
            "deposited": float(self.txt_deposited.text().replace(",", "") or 0),
            "place": self.txt_place.text(),
            "place_detail":self.txt_place_detail.text(),
            "photographer": self.txt_photographer.text(),
            "note": self.txt_note.toPlainText(),
        }

    def apply_style(self): # trang trí giao diện dialog
        self.setStyleSheet("""
            QDialog { background-color: #f5f6fa; }
            QGroupBox {
                font-family: 'Lexend'; font-size: 14px; font-weight: bold;
                color: #c23616; border: 1px solid #dcdde1;
                border-radius: 6px; margin-top: 12px; background-color: white;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QLabel { font-family: 'Lexend'; font-size: 12px; color: #2f3640; }
            QLineEdit, QComboBox,QPlainTextEdit {
                font-family: 'Lexend';
                font-size: 12px;
                padding: 6px;
                min-height: 28px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #3498db; }
            QLineEdit:read-only { background-color: #f1f2f6; color: #7f8fa6; }
            QPushButton { font-family: 'Lexend'; font-size: 13px; font-weight: bold; border-radius: 5px; padding: 8px 16px; }
            QPushButton#btn_save { background-color: #0097e6; color: white; border: none; }
            QPushButton#btn_save:hover { background-color: #00a8ff; }
            QPushButton#btn_cancel { background-color: #e1b12c; color: white; border: none; }
            QPushButton#btn_cancel:hover { background-color: #fbc531; }
        """)
