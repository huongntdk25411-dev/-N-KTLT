import sys
from PyQt6.QtWidgets import QApplication
# Import class từ file thực thi đăng nhập của bạn
from loginMainWindowEx import LoginMainWindowEx


def main():
    # Khởi tạo ứng dụng Qt
    app = QApplication(sys.argv)

    # Khởi tạo màn hình đăng nhập đầu tiên
    login_window = LoginMainWindowEx()

    # Hiển thị màn hình
    login_window.show()

    # Giữ ứng dụng chạy cho đến khi thoát
    sys.exit(app.exec())


if __name__ == "__main__":
    main()