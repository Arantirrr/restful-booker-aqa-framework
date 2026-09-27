
from clients.base_client import BaseClient


class AuthClient(BaseClient):

    def login(self, username, password):
        login_payload = {"username": username, "password": password}
        return self._post(path="/auth/login", json=login_payload)