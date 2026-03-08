import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap
# Import class từ file updateMainWindow.py mà bạn đã cung cấp
from updateMainWindow import Ui_AdminSettingsWindow


class AdminSettingsManager(QMainWindow):
    def __init__(self):
        super().__init__()


        self.ui = Ui_AdminSettingsWindow()
        self.ui.setupUi(self)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(current_dir, "..", "images", "logo.png")

        if os.path.exists(logo_path):
            self.ui.logoLabel.setPixmap(QPixmap(logo_path))
        else:
            print(f"Cảnh báo: Không tìm thấy logo tại {logo_path}")

        # 3. Kết nối các Signals & Slots
        self.ui.pushButtonSave.clicked.connect(self.handle_save_data)

    def handle_save_data(self):
        """Hàm xử lý khi nhấn nút Lưu và Cập nhật"""
        # Lấy dữ liệu từ các ô nhập liệu
        concept_name = self.ui.lineEditConceptName.text().strip()
        price = self.ui.lineEditPrice.text().strip()
        policy = self.ui.textEditPolicy.toPlainText().strip()

        # Kiểm tra dữ liệu đầu vào cơ bản
        if not concept_name or not price:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ Tên Concept và Giá!")
            return

        # Ở đây có thể thêm code để lưu vào database hoặc gửi lên Web
        print(f"Đang lưu Concept: {concept_name}")
        print(f"Giá: {price}")
        print(f"Chính sách: {policy[:1000]}...")

        # Hiển thị thông báo thành công
        QMessageBox.information(self, "Thành công", f"Đã cập nhật Concept '{concept_name}' thành công!")

        # Xóa trắng form sau khi lưu (tùy chọn)
        self.clear_form()

    def clear_form(self):
        """Hàm làm sạch các ô nhập liệu"""
        self.ui.lineEditConceptName.clear()
        self.ui.lineEditPrice.clear()
        self.ui.textEditPolicy.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = AdminSettingsManager()
    window.show()

    sys.exit(app.exec())