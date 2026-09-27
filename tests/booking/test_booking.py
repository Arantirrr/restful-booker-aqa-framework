from dataclasses import asdict

import requests
import pytest
from datetime import date, timedelta

from models.booking import BookingResponse, BookingRequest
from models.booking_errors import ValidationErrorResponse, ConflictErrorResponse


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.parametrize("room_id, total_price", [(10, 599), (11, 1999), (12, 50999)])
def test_create_booking_valid_data(booking_payload_factory, cleanup_bookings, room_id, total_price, booking_client):
    payload = booking_payload_factory(roomid=room_id, totalprice=total_price)
    response = booking_client.create(payload)
    assert response.status_code == requests.codes.created, f"Expected status code 201, received: {response.status_code}:{response.text}"
    assert response.headers["Content-Type"] == "application/json", f"Expected 'application/json', got {response.headers['Content-Type']}"
    response_booking = BookingResponse.model_validate(response.json())
    request_booking = BookingRequest.model_validate(payload)
    cleanup_bookings.append(response_booking.bookingid)
    assert response_booking.bookingdates == request_booking.bookingdates, f"Expected {request_booking.bookingdates}, got {response_booking.bookingdates}"
    assert response_booking.depositpaid == request_booking.depositpaid, f"Expected {request_booking.depositpaid}, got {response_booking.depositpaid}"
    assert response_booking.firstname == request_booking.firstname, f"Expected {request_booking.firstname}, got {response_booking.firstname}"
    assert response_booking.lastname == request_booking.lastname, f"Expected {request_booking.lastname}, got {response_booking.lastname}"
    assert response_booking.roomid == request_booking.roomid, f"Expected {request_booking.roomid}, got {response_booking.roomid}"

@pytest.mark.regression
@pytest.mark.positive
def test_get_booking_by_id(booking_data, created_booking, booking_client):
    payload = asdict(booking_data)
    response_0 = booking_client.get(created_booking)
    assert response_0.status_code == requests.codes.ok, f"Expected status 200, got {response_0.status_code}"
    assert response_0.headers["Content-Type"] == "application/json", f"Expected 'application/json', got {response_0.headers['Content-Type']}"
    response_booking_0 = BookingResponse.model_validate(response_0.json())
    request_booking = BookingRequest.model_validate(payload)
    assert response_booking_0.bookingdates == request_booking.bookingdates, f"Expected {request_booking.bookingdates}, got {response_booking_0.bookingdates}"
    assert response_booking_0.depositpaid == request_booking.depositpaid, f"Expected {request_booking.depositpaid}, got {response_booking_0.depositpaid}"
    assert response_booking_0.firstname == request_booking.firstname, f"Expected {request_booking.firstname}, got {response_booking_0.firstname}"
    assert response_booking_0.lastname == request_booking.lastname, f"Expected {request_booking.lastname}, got {response_booking_0.lastname}"
    assert response_booking_0.roomid == request_booking.roomid, f"Expected {request_booking.roomid}, got {response_booking_0.roomid}"
    assert response_booking_0.bookingid == created_booking, f"Expected {created_booking}, got: {response_booking_0.bookingid}"

    response_1 = booking_client.get(created_booking)
    response_booking_1 = BookingResponse.model_validate(response_1.json())
    assert response_booking_0 == response_booking_1, "Two GETs returned different results"

@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("missing_field, expected_error", [
    ("firstname", ["Firstname should not be blank"]),
    ("lastname", ["Lastname should not be blank"]),
    (("firstname", "lastname"), ['Firstname should not be blank', 'Lastname should not be blank']),
])
def test_create_booking_invalid_data(booking_payload_factory, missing_field, expected_error, booking_client):
    payload = booking_payload_factory(exclude=missing_field)
    response = booking_client.create(payload)
    assert response.status_code == requests.codes.bad, f"Expected status 400, got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", f"Expected 'application/json', got {response.headers['Content-Type']}"
    response_errors = ValidationErrorResponse.model_validate(response.json())
    assert sorted(response_errors.errors) == sorted(expected_error)

@pytest.mark.regression
@pytest.mark.negative
def test_create_booking_with_invalid_dates(booking_payload_factory, booking_client):
    # Checks that server rejects when checkout is before checkin and in the past
    payload = booking_payload_factory(
        bookingdates={
            "checkin": (date.today() + timedelta(days=1)).isoformat(),
            "checkout": (date.today() + timedelta(days=-1)).isoformat(),
        }
    )
    response = booking_client.create(payload)
    assert response.status_code == requests.codes.conflict, f"Expected status 409, got {response.status_code}"
    assert response.headers["Content-Type"] == "application/json", f"Expected 'application/json', got {response.headers['Content-Type']}"
    response_error = ConflictErrorResponse.model_validate(response.json())
    assert response_error.error == "Failed to create booking", f"Expected msg 'Failed to create booking', got {response_error.error}"

@pytest.mark.regression
@pytest.mark.negative
def test_create_booking_with_nonexistent_room(booking_payload_factory, cleanup_bookings, booking_client):
    payload = booking_payload_factory(roomid=99999999)
    response = booking_client.create(payload)
    # BUG: should be 400/404, actual = 201
    assert response.status_code == requests.codes.created
    response_booking = BookingResponse.model_validate(response.json())
    cleanup_bookings.append(response_booking.bookingid)

