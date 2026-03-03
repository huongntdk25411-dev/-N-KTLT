import sqlite3
import os


class DatabaseManager:
    def __init__(self):
        # Đảm bảo thư mục dataset tồn tại
        if not os.path.exists('dataset'):
            os.makedirs('dataset')

        # Kết nối tới file DB trong thư mục dataset
        self.db_path = 'dataset/new_year_photo.db'
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Tạo bảng users lưu thông tin và giới tính"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                gender TEXT
            )
        ''')
        self.conn.commit()

    def register_user(self, name, user, email, pwd, gender):
        """Hàm lưu người dùng mới"""
        try:
            self.cursor.execute(
                "INSERT INTO users (fullname, username, email, password, gender) VALUES (?, ?, ?, ?, ?)",
                (name, user, email, pwd, gender)
            )
            self.conn.commit()
            return True, f"Chào mừng {name} đã đến với New Year Photo!"
        except sqlite3.IntegrityError:
            return False, "Tên đăng nhập hoặc Email đã tồn tại!"

    def check_email_exists(self, email):
        """Kiểm tra email để phục vụ flow quên mật khẩu"""
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        return self.cursor.fetchone() is not None

    def update_password(self, email, new_pwd):
        """Cập nhật mật khẩu mới sau khi reset"""
        try:
            self.cursor.execute("UPDATE users SET password=? WHERE email=?", (new_pwd, email))
            self.conn.commit()
            return True
        except Exception:
            return False





    def login_user(self, email, password):
        """Kiểm tra thông tin đăng nhập từ database"""
        self.cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = self.cursor.fetchone()
        if user:
            return True, user[1]  # Trả về True và Fullname của người dùng
        return False, None