from PyQt6.QtCore import QDate, QTime
import json
import os

class FileFactory:

    def writeData(self, path, arrData):
        jsonString = json.dumps(
            [
                {
                    "name": item.name,
                    "email": item.email,
                    "phone": item.phone,
                    "date": item.date.toString("yyyy-MM-dd"),
                    "time": item.time.toString("HH:mm"),
                    "concept": item.concept,
                    "location": item.location
                }
                for item in arrData
            ],
            indent=4,
            ensure_ascii=False   # 👈 quan trọng để lưu tiếng Việt
        )

        with open(path, "w", encoding="utf-8") as f:   # 👈 FIX
            f.write(jsonString)


    def readData(self, path, ClassName):
        if not os.path.isfile(path):
            return []

        with open(path, "r", encoding="utf-8") as f:   # 👈 FIX
            arr = json.load(f)

        result = []

        for item in arr:
            date_obj = QDate.fromString(item["date"], "yyyy-MM-dd")
            time_obj = QTime.fromString(item["time"], "HH:mm")

            booking = ClassName(
                item["name"],
                item["email"],
                item["phone"],
                date_obj,
                time_obj,
                item["concept"],
                item["location"]
            )

            result.append(booking)

        return result
