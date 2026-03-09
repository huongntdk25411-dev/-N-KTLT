from PyQt6.QtWidgets import QApplication
from models.admin.feature_customer_management.ui.EditCustomerDialog import EditCustomerDialog

app = QApplication([])

# Tạo customer mẫu để test
customer = {
    "name":"Mộng Hoài",
    "phone":"0987777666",
    "email":"monghoai@gmail.com",
    "date":"2019-09-30",
    "time":"9:00",
    "concept":"Chụp kỷ yếu",
    "background":"Ngoài trời",
    "status":"Đã cọc",
    "total_fee":15000000,
    "deposited":200000,
    "place":"TP. Hồ Chí Minh",
    "place_detail":"Trường THPT Nguyễn Thị Minh Khai",
    "photographer":"Bình Minh",
    "note":"Khách test",
    "password":"123"
}

w = EditCustomerDialog(customer)
w.show()

app.exec()