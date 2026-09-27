import pytest

from dataclasses import asdict
from datetime import date, timedelta
from clients.booking_client import BookingClient
from models.booking import BookingResponse
from tests.data.booking_data import BookingData, BookingDatesData



@pytest.fixture(scope="session")
def booking_client(settings, token):
    return BookingClient(settings.api_url, token)

@pytest.fixture
def cleanup_bookings(booking_client):
    ids = []
    yield ids
    for booking_id in ids:
        booking_client.delete(booking_id)

@pytest.fixture
def created_booking(booking_data, booking_client):
    response = booking_client.create(asdict(booking_data))
    booking_id = BookingResponse.model_validate(response.json()).bookingid
    yield booking_id
    booking_client.delete(booking_id)

@pytest.fixture
def booking_payload_factory(booking_data):
    def factory(*, exclude=None, **kwargs):
        payload = asdict(booking_data)
        payload.update(kwargs)
        if exclude is None:
            exclude = ()
        elif isinstance(exclude, str):
            exclude = (exclude,)
        for field in exclude:
            payload.pop(field, None)
        return payload
    return factory

@pytest.fixture
def booking_data():
    today = date.today()
    return BookingData(
        roomid=10,
        firstname="FirstName",
        lastname="LastName",
        totalprice=2999,
        depositpaid=False,
        bookingdates=BookingDatesData(
            checkin=(today + timedelta(days=1)).isoformat(),
            checkout=(today + timedelta(days=3)).isoformat()
        ),
        email="email@gmail.com",
        phone="89889931320"
    )
