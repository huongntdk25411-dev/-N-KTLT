from PyQt6.QtWidgets import QApplication
from feature_customer_management.ui.EditCustomerDialog import EditCustomerDialog
from feature_customer_management.models.customer import Customer

app = QApplication([])

# Tạo customer mẫu để test
customer = Customer("KH009","Test User","0900000000","test@gmail.com","Chụp thử","Đã cọc",10000000,3000000,"Studio","Test Photo","Khách test dialog","testuser","123",""
)

w = EditCustomerDialog(customer)
w.show()

app.exec()