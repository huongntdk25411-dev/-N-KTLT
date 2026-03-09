import datetime
class Customer:
    def __init__(self,date,time,name,email,phone,concept,background="",place="",place_detail="",note="",service="",status=None,total_fee=None,deposited=0,photographer="",login_email="",password=""):
        # thông tin cá nhân cơ bản
        self.name=name
        self.phone=phone
        self.email=email
        # thông tin gói chụp
        self.concept=concept
        self.status=status
        self.background = background
        self.place = place
        self.place_detail = place_detail
        self.note=note
        self.service=service
        # thông tin lịch đặt
        self.date=date
        self.time=time
        self.total_fee=float(total_fee)
        self.deposited=float(deposited)
        self.unpaid()
        self.photographer=photographer
        # thông tin hồ sơ KH trên hệ thống
        self.login_email=login_email
        self.password=password

    def unpaid(self): #tiền chưa thanh toán
        return float(self.total_fee) - float(self.deposited)
    def to_dict(self): # chuyển object thành dict để lưu file json
        return self.__dict__