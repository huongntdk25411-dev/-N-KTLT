class Booking:
    def __init__(self, name, email, phone, date, time, concept, location):
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        self.concept = concept
        self.location = location

    def __str__(self):
        return f"{self.time.toString('HH:mm')} - {self.name}\t{self.concept}\t{self.location}"




