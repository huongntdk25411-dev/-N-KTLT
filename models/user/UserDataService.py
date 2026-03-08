import json
from pathlib import Path


class UserDataService:
    def __init__(self):
        current_path = Path(__file__).resolve()

        # Tìm thư mục chứa datasets
        PROJECT_ROOT = None
        for parent in current_path.parents:
            if (parent / "datasets").exists():
                PROJECT_ROOT = parent
                break

        if PROJECT_ROOT is None:
            raise Exception("Không tìm thấy thư mục datasets")

        self.bookings_file = PROJECT_ROOT / "datasets" / "bookings.json"

    def get_all_bookings(self):
        if not self.bookings_file.exists():
            return []

        try:
            with open(self.bookings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def filter_by_phone(self, phone_search):
        """Lọc chính xác theo số điện thoại"""
        all_bookings = self.get_all_bookings()

        # So sánh chính xác, không dùng 'in'
        return [
            b for b in all_bookings
            if str(b.get("phone", "")).strip() == phone_search.strip()
        ]