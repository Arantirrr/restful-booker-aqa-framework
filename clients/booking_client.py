
from clients.base_client import BaseClient


class BookingClient(BaseClient):

    def create(self, payload):
        return self._post(path="/booking", json=payload)

    def get(self, booking_id):
        return self._get(path=f"/booking/{booking_id}")

    def delete(self, booking_id):
        return self._delete(path=f"/booking/{booking_id}")