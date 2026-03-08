import datetime
import json
import os
import csv

from models.admin.feature_customer_management.models.customer import Customer


class Customers:
    def __init__(self, filepath=None):
        if filepath is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.filepath = os.path.join(base_dir, "..", "datasets", "data_customers.json")
            self.filepath = os.path.normpath(self.filepath)
        else:
            self.filepath = filepath

        self.list_customers = []
        self.load_data()

    def load_data(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))

        # đi về thư mục gốc FINALPROJECT
        project_root = os.path.abspath(
            os.path.join(base_dir, "..", "..", "..", "..")
        )

        csv_path = os.path.join(project_root, "datasets", "customerin4.csv")
        json_path = os.path.join(project_root, "datasets", "bookings.json")

        self.list_customers = []

        bookings_data = []
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                bookings_data = json.load(f)

        if not os.path.exists(csv_path):
            print("Không tìm thấy CSV:", csv_path)
            return

        with open(csv_path, "r", encoding="utf-8-sig") as f:

            reader = csv.DictReader(f)

            for i, row in enumerate(reader, start=1):

                booking = None
                for b in bookings_data:
                    if b.get("email") == row.get("Email"):
                        booking = b
                        break

                concept = booking.get("concept", "") if booking else ""
                location = booking.get("place", "") if booking else ""
                note = booking.get("note", "") if booking else ""

                item = Customer(
                    name=row.get("Họ và tên", ""),
                    phone=row.get("Số điện thoại", ""),
                    email=row.get("Email", ""),
                    concept=concept,
                    status="Đã xác nhận",
                    total_fee=0,
                    deposited=0,
                    location=location,
                    photographer="",
                    note=note,
                    username=row.get("Email", ""),
                    password=row.get("Mật khẩu", ""),
                    last_login=""
                )

                self.list_customers.append(item)

    def save_data(self):  # chuyển danh sách đối tượng sang dict để lưu json
        data = []
        for c in self.list_customers:
            data.append(c.to_dict())

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def sort_data(self):  # sort by status
        def priority(customer):
            if customer.status == "Đã cọc":
                return 0
            if customer.status == "Đã hủy":
                return 2
            return 1

        self.list_customers.sort(key=lambda c: priority(c), reverse=False)

    def search_customers(self, keyword):
        keyword = keyword.lower()
        results = []

        for c in self.list_customers:
            if (keyword in c.name.lower() or
                    keyword in str(c.phone) or
                    keyword in str(c.email).lower()):
                results.append(c)

        return results

    def remove_by_phone(self, phone):
        new_list = []

        for c in self.list_customers:
            if c.phone != phone:
                new_list.append(c)

        self.list_customers = new_list
        self.save_data()

    def update_last_login(self, username):
        for c in self.list_customers:
            if c.username == username:
                c.last_login = datetime.datetime.now().isoformat()
                break

        self.save_data()

    def get_all(self):
        return self.list_customers