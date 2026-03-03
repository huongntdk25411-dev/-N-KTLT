from PyQt6.QtCore import QDate, QTime

from Final.timeDateEdit_Customers.Dataset import Dataset
from Final.timeDateEdit_Customers.FileFactory import FileFactory
from Final.timeDateEdit_Customers.models.Booking import Booking

ds = Dataset()

ds = Dataset()

ds.add(Booking("Nguyễn Minh Anh","anh01@gmail.com","0909000001",QDate(2026,2,10),QTime(8,0),"Tết cổ truyền","TP.HCM"))
ds.add(Booking("Trần Hoàng Nam","nam02@gmail.com","0909000002",QDate(2026,2,10),QTime(10,0),"Tết cổ truyền","TP.HCM"))
ds.add(Booking("Lê Thu Hà","ha03@gmail.com","0909000003",QDate(2026,2,10),QTime(13,0),"Tết cổ truyền","TP.HCM"))
ds.add(Booking("Phạm Quốc Bảo","bao04@gmail.com","0909000004",QDate(2026,2,10),QTime(15,0),"Tết cổ truyền","TP.HCM"))
ds.add(Booking("Đỗ Mỹ Linh","linh05@gmail.com","0909000005",QDate(2026,2,10),QTime(17,0),"Tết cổ truyền","TP.HCM"))

ds.add(Booking("Võ Gia Huy","huy06@gmail.com","0909000006",QDate(2026,2,12),QTime(8,0),"Vintage","TP.HCM"))
ds.add(Booking("Bùi Thanh Trúc","truc07@gmail.com","0909000007",QDate(2026,2,12),QTime(10,0),"Vintage","TP.HCM"))
ds.add(Booking("Ngô Đức Thịnh","thinh08@gmail.com","0909000008",QDate(2026,2,12),QTime(13,0),"Vintage","TP.HCM"))

ds.add(Booking("Huỳnh Khánh Vy","vy09@gmail.com","0909000009",QDate(2026,2,14),QTime(8,0),"Valentine","TP.HCM"))
ds.add(Booking("Phan Tuấn Kiệt","kiet10@gmail.com","0909000010",QDate(2026,2,14),QTime(10,0),"Valentine","TP.HCM"))
ds.add(Booking("Trương Ngọc Mai","mai11@gmail.com","0909000011",QDate(2026,2,14),QTime(13,0),"Valentine","TP.HCM"))
ds.add(Booking("Đặng Hoài Nam","nam12@gmail.com","0909000012",QDate(2026,2,14),QTime(15,0),"Valentine","TP.HCM"))
ds.add(Booking("Lý Thảo Nhi","nhi13@gmail.com","0909000013",QDate(2026,2,14),QTime(17,0),"Valentine","TP.HCM"))

ds.add(Booking("Nguyễn Quốc Khánh","khanh14@gmail.com","0909000014",QDate(2026,2,16),QTime(8,0),"Gia đình","TP.HCM"))
ds.add(Booking("Trần Gia Linh","linh15@gmail.com","0909000015",QDate(2026,2,16),QTime(10,0),"Gia đình","TP.HCM"))

ds.add(Booking("Phạm Minh Khoa","khoa16@gmail.com","0909000016",QDate(2026,2,18),QTime(8,0),"Ngoại cảnh","TP.HCM"))
ds.add(Booking("Đoàn Thùy Dương","duong17@gmail.com","0909000017",QDate(2026,2,18),QTime(10,0),"Ngoại cảnh","TP.HCM"))
ds.add(Booking("Nguyễn Hải Đăng","dang18@gmail.com","0909000018",QDate(2026,2,18),QTime(13,0),"Ngoại cảnh","TP.HCM"))

ds.add(Booking("Lê Nhật Quang","quang19@gmail.com","0909000019",QDate(2026,2,20),QTime(8,0),"Couple","TP.HCM"))
ds.add(Booking("Vũ Kim Chi","chi20@gmail.com","0909000020",QDate(2026,2,20),QTime(10,0),"Couple","TP.HCM"))
ds.add(Booking("Trịnh Thanh Bình","binh21@gmail.com","0909000021",QDate(2026,2,20),QTime(13,0),"Couple","TP.HCM"))
ds.add(Booking("Phùng Gia Hân","han22@gmail.com","0909000022",QDate(2026,2,20),QTime(15,0),"Couple","TP.HCM"))

ds.add(Booking("Hoàng Đức Anh","anh23@gmail.com","0909000023",QDate(2026,2,22),QTime(8,0),"Profile","TP.HCM"))
ds.add(Booking("Tạ Ngọc Ánh","anh24@gmail.com","0909000024",QDate(2026,2,22),QTime(10,0),"Profile","TP.HCM"))
ds.add(Booking("Cao Hoài Phương","phuong25@gmail.com","0909000025",QDate(2026,2,22),QTime(13,0),"Profile","TP.HCM"))
ds.add(Booking("Mai Anh Tuấn","tuan26@gmail.com","0909000026",QDate(2026,2,22),QTime(15,0),"Profile","TP.HCM"))
ds.add(Booking("Lương Bảo Trân","tran27@gmail.com","0909000027",QDate(2026,2,22),QTime(17,0),"Profile","TP.HCM"))

ds.add(Booking("Đinh Minh Tuấn","tuan28@gmail.com","0909000028",QDate(2026,2,25),QTime(8,0),"Doanh nhân","TP.HCM"))
ds.add(Booking("Nguyễn Hồng Nhung","nhung29@gmail.com","0909000029",QDate(2026,2,25),QTime(10,0),"Doanh nhân","TP.HCM"))
ds.add(Booking("Phạm Thái Sơn","son30@gmail.com","0909000030",QDate(2026,2,25),QTime(13,0),"Doanh nhân","TP.HCM"))


ff=FileFactory()

ff.writeData("../dataset/database.json", ds.bookings)
