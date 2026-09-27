from pydantic import BaseModel

class BookingDates(BaseModel):
    checkin: str
    checkout: str

class BookingBase(BaseModel):
    roomid: int
    firstname: str
    lastname: str
    depositpaid: bool
    bookingdates: BookingDates

class BookingRequest(BookingBase):
    totalprice: int
    email: str
    phone: str

class BookingResponse(BookingBase):
    bookingid: int