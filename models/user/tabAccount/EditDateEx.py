import json
import os
from PyQt6.QtWidgets import QMessageBox

from models.user.tabAccount.EditDate import Ui_MainWindow


class EditDateEx(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
        self.filename = os.path.join(project_root, "datasets", "bookings.json")

        self.original_data = None
        self.refresh_callback = None

        self.pushButtonBook.clicked.connect(self.process_update)

    def load_data(self, data):
        self.original_data = data

        self.lineEditName.setText(data.get("name", ""))
        self.lineEditEmail.setText(data.get("email", ""))
        self.lineEditPhone.setText(data.get("phone", ""))

        self.comboBoxConcept.setCurrentText(data.get("concept", ""))
        self.comboBoxConcept_2.setCurrentText(data.get("background", ""))
        self.comboBoxConceptPlace.setCurrentText(data.get("place", ""))
        self.lineEditPlace2.setText(data.get("place_detail", ""))
        self.textEditNote.setPlainText(data.get("note", ""))

        from PyQt6.QtCore import QDate, QTime

        try:
            day, month, year = map(int, data["date"].split("/"))
            self.dateEdit.setDate(QDate(year, month, day))

            hour, minute = map(int, data["time"].split(":"))
            self.timeEdit.setTime(QTime(hour, minute))
        except:
            pass

    def process_update(self):
        name = self.lineEditName.text()
        email = self.lineEditEmail.text()
        phone = self.lineEditPhone.text()

        if name == "" or email == "" or phone == "":
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        new_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "concept": self.comboBoxConcept.currentText(),
            "background": self.comboBoxConcept_2.currentText(),
            "place": self.comboBoxConceptPlace.currentText(),
            "place_detail": self.lineEditPlace2.text(),
            "date": self.dateEdit.date().toString("dd/MM/yyyy"),
            "time": self.timeEdit.time().toString("HH:mm"),
            "service": "Không chọn",
            "note": self.textEditNote.toPlainText()
        }

        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                file_data = json.load(f)
        else:
            file_data = []

        updated = False

        for i, item in enumerate(file_data):
            if (
                item.get("email") == self.original_data.get("email")
                and item.get("date") == self.original_data.get("date")
                and item.get("time") == self.original_data.get("time")
            ):
                file_data[i] = new_data
                updated = True
                break

        if not updated:
            file_data.append(new_data)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(file_data, f, ensure_ascii=False, indent=4)

        QMessageBox.information(self.MainWindow, "Thành công", "Cập nhật thành công")

        if self.refresh_callback:
            self.refresh_callback()

        self.MainWindow.close()