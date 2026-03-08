from models.admin.feature_customer_management.models.customer import Customer
from models.admin.feature_customer_management.models.customers import Customers

cs=Customers()
# remove all old datas
cs.list_customers=[]

c1=Customer("KH001","Trấn Thành","0908789999","tranthanh@tt.com.vn","Chụp cưới","Đã cọc",15000000,500000,"Đà Lạt","Hari Won","Yêu cầu chụp ngoài trời","tranthanhtown","12345","")

c2=Customer("KH002","Trường Giang","0809789666","truonggiang@giangtr.vn","Chụp gia đình","Đã xác nhận",800000,0,"TP. Hồ Chí Minh","Nhã Phương","Chụp trong studio","gianggiang","78910","")

c3=Customer("KH003","Victor Vũ","0789222444","victorvu@vuvic.vn","Phóng sự sự kiện","Đã hủy","12000000","200000","Hà Nội","Ngọc Diệp","Khách hủy do đổi lịch","victor","vuvic123","")

# thêm vô danh sách
cs.list_customers.extend([c1,c2,c3])
# sắp xếp theo status
cs.sort_data()
#lưu file json
cs.save_data()

print("Đã tạo dữ liệu thành công")