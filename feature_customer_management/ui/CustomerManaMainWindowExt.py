from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox,QMainWindow

from feature_customer_management.models.customers import Customers
from feature_customer_management.ui.CustomerManaMainWindow import Ui_MainWindow
from feature_customer_management.ui.EditCustomerDialog import EditCustomerDialog


class CustomerManaMainWindowExt(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.customers_manager=Customers()
        self.customers_manager.sort_data()

        self.setupSignalandSlot()
        self.displayList(self.customers_manager.list_customers)
        self.labelDetail.setText("Chưa chọn khách hàng")

    def setupSignalandSlot(self):
        self.pushButtonSearch.clicked.connect(self.process_search)
        self.lineEditSearch.textChanged.connect(self.process_search)
        self.tableWidgetCustomerInfo.cellClicked.connect(self.displayDetails)
        self.pushButtonRemove.clicked.connect(self.process_remove)
        self.pushButtonEdit.clicked.connect(self.process_adjust)

    def displayList(self,customer_list):
        self.labelTotal.setText(f"Tổng cộng: {len(customer_list)} Khách hàng")
        # reset table
        self.tableWidgetCustomerInfo.setRowCount(0)

        for row,customer in enumerate(customer_list):
            self.tableWidgetCustomerInfo.insertRow(row)
            self.tableWidgetCustomerInfo.setItem(row,0,QTableWidgetItem(str(customer.id)))
            self.tableWidgetCustomerInfo.setItem(row,1,QTableWidgetItem(customer.name))
            self.tableWidgetCustomerInfo.setItem(row,2,QTableWidgetItem(customer.concept))
            self.tableWidgetCustomerInfo.setItem(row,3,QTableWidgetItem(customer.status))

            money_str="{:,.0f}đ".format(customer.total_fee)
            self.tableWidgetCustomerInfo.setItem(row,4,QTableWidgetItem(money_str))


    def displayDetails(self,row,col):
        #1. lấy ID từ cột đầu tiên (cột 0) của dòng đang chọn
        selected_id=self.tableWidgetCustomerInfo.item(row,0).text()
        #2. tạo 1 biến tạm để chứa khách hàng tìm được
        target_customer=None
        #3. duyệt danh sách khách hàng để tìm người có ID khớp
        for c in self.customers_manager.list_customers:
            if str(c.id)==selected_id:
                target_customer=c # Nếu tìm thấy, gán đối tượng c vào biến target
                break # đã tìm thấy thì thoát vòng lặp
        #4. nếu tìm thấy khách hàng, hiển thị thông tin lên nhãn
        if target_customer is not None:
            # Tạo chuỗi thông tin
            info = (
                f"--THÔNG TIN CHI TIẾT--\n\n"
                f"1. Thông tin cá nhân:\n"
                f" - ID: {target_customer.id}\n"
                f" - Tên Khách hàng: {target_customer.name}\n"
                f" - Số điện thoại: {target_customer.phone}\n"
                f" - Email: {target_customer.email}\n\n"
                
                f"2. Thông tin đặt lịch:\n"
                f" - Gói chụp: {target_customer.concept}\n"
                f" - Địa điểm: {target_customer.location}\n"
                f" - Thợ chụp: {target_customer.photographer}\n"
                f" - Trạng thái: {target_customer.status}\n"
                f" - Ghi chú thêm: {target_customer.note}\n\n"

                f"3. Chi phí:\n"
                f" - Tổng chi phí (đ):{'{:,.0f}'.format(target_customer.total_fee)}đ\n"
                f" - Đã cọc: {'{:,.0f}'.format(target_customer.deposited)}đ\n"
                f" - Chưa thanh toán: {'{:,.0f}'.format(target_customer.unpaid())}đ\n\n"
                
                f"4. Thông tin tài khoản\n"
                f" - Tên đăng nhập: {target_customer.username}\n"
                f" - Lần cuối đăng nhập: {target_customer.get_last_login_display()}\n"
            )

            #4. Cập nhật nội dung cho Label ở cột bên phải
            self.labelDetail.setText(info)

    def process_search(self):
        keyword=self.lineEditSearch.text()
        result=self.customers_manager.search_customers(keyword)

        self.displayList(result)
        #reset lại detail sau khi search
        self.labelDetail.setText("Chưa chọn khách hàng")

    def process_adjust(self): # mở dialog Edit & đồng bộ kết quả trả về
        current_row=self.tableWidgetCustomerInfo.currentRow()
        if current_row<0:
            QMessageBox.warning(self,"Thông báo","Vui lòng chọn khách hàng cần chỉnh sửa!")
            return

        selected_id=self.tableWidgetCustomerInfo.item(current_row,0).text()
        target_customer=None
        for c in self.customers_manager.list_customers:
            if str(c.id)==selected_id:
                target_customer=c
                break
        if target_customer is not None:
            dialog=EditCustomerDialog(target_customer,self)

            if dialog.exec():
                data=dialog.get_data()
                target_customer.id=data["id"]
                target_customer.name=data["name"]
                target_customer.phone=data["phone"]
                target_customer.email=data["email"]

                target_customer.concept=data["concept"]
                target_customer.photographer=data["photographer"]
                target_customer.location=data["location"]
                target_customer.status=data["status"]
                target_customer.total_fee=data["total_fee"]
                target_customer.deposited=data["deposited"]

                target_customer.note=data["note"]

                target_customer.username=data["username"]
                target_customer.password=data["password"]
                # target_customer.last_login=data["last_login"] -> ko đc sửa

                # save and sorting
                self.customers_manager.save_data()
                self.customers_manager.sort_data()

                # update table
                self.displayList(self.customers_manager.list_customers)
                # LIÊN KẾT: Tìm lại dòng mới sau khi sort để cập nhật lại Label
                for row in range(self.tableWidgetCustomerInfo.rowCount()):
                    if self.tableWidgetCustomerInfo.item(row, 0).text() == selected_id:
                        self.displayDetails(row, 0)  # Cập nhật Label
                        self.tableWidgetCustomerInfo.selectRow(row)  # Highlight dòng đó
                        break

                QMessageBox.information(self, "Thành công", "Đã cập nhật dữ liệu đồng bộ")

    def process_remove(self):
        # Lấy dòng đc chọn
        cur_row=self.tableWidgetCustomerInfo.currentRow()
        if cur_row<0:
            QMessageBox.warning(self,"Cảnh báo","Vui lòng chọn 1 Khách hàng trên bảng để xóa")
            return

        selected_id=self.tableWidgetCustomerInfo.item(cur_row,0).text()
        reply=QMessageBox.question(self,"Xác nhận",f"Bạn có chắc chắn muốn xóa khách hàng {selected_id}?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # thực hiện xóa trong dữ liệu
            self.customers_manager.remove_by_id(selected_id)
            # cập nhật lại bảng và tìm kiếm
            self.process_search()
            # LIÊN KẾT: xóa trắng label chi tiết
            self.labelDetail.setText("Chưa chọn khách hàng")
            QMessageBox.information(self,"Thành công","Đã xóa khách hàng")
