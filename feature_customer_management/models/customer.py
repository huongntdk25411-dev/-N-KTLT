import datetime


class Customer:
    def __init__(self,id,name,phone,email,concept,status,total_fee,deposited=0,location="",photographer="",note="",username="",password="",last_login=""):
        # thông tin cá nhân cơ bản
        self.id=id
        self.name=name
        self.phone=phone
        self.email=email
        # thông tin đặt lịch
        self.concept=concept
        self.status=status
        self.total_fee=total_fee
        self.deposited=deposited
        self.location=location
        self.photographer=photographer
        self.note=note
        # thông tin hồ sơ KH trên hệ thống
        self.username=username
        self.password=password
        self.last_login=last_login
    def unpaid(self): #tiền chưa thanh toán
        return self.total_fee - self.deposited
    def to_dict(self): # chuyển object thành dict để lưu file json
        return self.__dict__
    def get_last_login_display(self):
        try:
            dt = datetime.fromisoformat(self.last_login)
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except:
            return self.last_login