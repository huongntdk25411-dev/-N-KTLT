class CustomerBooking:
    def __init__(self,
                 name="",
                 email="",
                 phone="",
                 concept="",
                 background="",
                 place="",
                 place_detail="",
                 note="",
                 service=""):

        self.name = name
        self.email = email
        self.phone = phone
        self.concept = concept
        self.background = background
        self.place = place
        self.place_detail=place_detail
        self.note = note
        self.service=service

    def __str__(self):
        return f"{self.name} - {self.phone}"
