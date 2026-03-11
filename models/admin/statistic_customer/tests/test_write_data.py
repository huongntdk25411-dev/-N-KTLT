import json
import random
from datetime import datetime, timedelta

names = [
"Nguyễn Minh Anh","Trần Hoàng Nam","Lê Thu Hà","Phạm Quốc Bảo","Đỗ Mỹ Linh",
"Võ Gia Huy","Bùi Thanh Trúc","Ngô Đức Thịnh","Huỳnh Khánh Vy","Phan Tuấn Kiệt",
"Trương Ngọc Mai","Đặng Hoài Nam","Lý Thảo Nhi","Nguyễn Quốc Khánh","Trần Gia Linh",
"Phạm Minh Khoa","Đoàn Thùy Dương","Nguyễn Hải Đăng","Lê Nhật Quang","Vũ Kim Chi",
"Trịnh Thanh Bình","Phùng Gia Hân","Hoàng Đức Anh","Tạ Ngọc Ánh","Cao Hoài Phương"
]

concepts = [
"Cá nhân",
"Gia đình",
"Cặp đôi",
"Sự kiện",
"HSSV(Kỷ yếu, Tốt nghiệp,..)",
"Ảnh nhóm",
"Ảnh thẻ"
]

backgrounds = ["Studio", "Ngoài trời"]

places = [
"TP.HCM",
"Hà Nội",
"Đà Nẵng",
"Lâm Đồng",
"Cần Thơ"
]

times = [
"08:00","10:00","13:00","15:00","17:00","19:00"
]

services = [
"Không chọn",
"Make-up + Làm tóc"
]

start_date = datetime(2026,1,1)
end_date = datetime(2026,6,30)

bookings = []
used_slots = set()

while len(bookings) < 250:

    random_days = random.randint(0,(end_date-start_date).days)
    date = start_date + timedelta(days=random_days)

    time = random.choice(times)

    key = (date.strftime("%d/%m/%Y"), time)

    if key in used_slots:
        continue

    used_slots.add(key)

    booking = {
        "date": date.strftime("%d/%m/%Y"),
        "time": time,
        "name": random.choice(names),
        "email": f"user{len(bookings)+1}@gmail.com",
        "phone": "09" + str(random.randint(10000000,99999999)),
        "concept": random.choice(concepts),
        "background": random.choice(backgrounds),
        "place": random.choice(places),
        "place_detail": "",
        "note": "",
        "service": random.choice(services)
    }

    bookings.append(booking)

with open("../data/bookings.json", "w", encoding="utf-8") as f:
    json.dump(bookings,f,ensure_ascii=False,indent=4)
