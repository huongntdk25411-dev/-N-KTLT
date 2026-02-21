class Dataset:
    def __init__(self):
        self.bookings = []

    def add(self, booking):
        self.bookings.append(booking)

    def get_bookings_by_date(self, date):
        return [b for b in self.bookings if b.date == date]

    def is_full_date(self, date, max_slots=5):
        return len(self.get_bookings_by_date(date)) >= max_slots

    def remove_booking(self, booking):
        self.bookings.remove(booking)
