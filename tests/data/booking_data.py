from dataclasses import dataclass


@dataclass(frozen=True)
class BookingDatesData:
    checkin: str
    checkout: str

@dataclass(frozen=True)
class BookingData:
    roomid: int
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    email: str
    phone: str
    bookingdates: BookingDatesData