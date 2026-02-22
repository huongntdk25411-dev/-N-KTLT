import datetime
import json
import os

from feature_customer_management.models.customer import Customer


class Customers:
    def __init__(self,filepath=None):
        if filepath is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.filepath = os.path.join(base_dir, "..", "datasets", "data_customers.json")
            self.filepath = os.path.normpath(self.filepath)
        else:
            self.filepath = filepath

        self.list_customers = []
        self.load_data()

    def load_data(self): # read json file and make list object customers
        if not os.path.exists(self.filepath):
            self.list_customers = []
            return
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.list_customers=[]
            for d in data:
                # tạo mới đối tượng customer từ dict và thêm vào danh sách
                item=Customer(
                    id=d.get("id", ""),
                    name=d.get("name", ""),
                    phone=d.get("phone", ""),
                    email=d.get("email", ""),

                    concept=d.get("concept", ""),
                    status=d.get("status", ""),
                    total_fee=float(d.get("total_fee", 0)),
                    deposited=float(d.get("deposited", 0)),
                    location=d.get("location", ""),
                    photographer=d.get("photographer", ""),
                    note=d.get("note", ""),

                    username=d.get("username", ""),
                    password=d.get("password", ""),
                    last_login=d.get("last_login", "")
                )
                self.list_customers.append(item)

    def save_data(self): # chuyển danh sách đô tượng sang danh sách dict để lưu json file
        data=[]
        for c in self.list_customers:
            data.append(c.to_dict())

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def sort_data(self): # sort by status: deposited -> confirmed -> canceled
        def priority(customer):
            if customer.status=="Đã cọc":
                return 0
            if customer.status=="Đã hủy":
                return 2
            return 1
        self.list_customers.sort(key=lambda c:priority(c), reverse=False)

    def search_customers(self,keyword):
        keyword=keyword.lower()
        results=[]
        for c in self.list_customers:
            if (keyword in c.name.lower() or
                    keyword in str(c.phone) or
                    keyword in str(c.id).lower()):
                results.append(c)
        return results

    def remove_by_id(self,customer_id): #tìm và xóa khách hàng có ID tương ứng
        new_list=[]
        for c in self.list_customers:
            if c.id != customer_id:
                new_list.append(c)
        self.list_customers=new_list
        self.save_data()

    def update_last_login(self,username):
        for c in self.list_customers:
            if c.username == username:
                c.last_login=datetime.datetime.now().isoformat()
                break
        self.save_data()
