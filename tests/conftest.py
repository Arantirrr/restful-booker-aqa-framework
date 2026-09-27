
import pytest

from clients.auth_client import AuthClient

@pytest.fixture(scope="session")
def auth_client(settings):
    return AuthClient(settings.api_url)

@pytest.fixture(scope="session")
def token(settings, auth_client):
    return auth_client.login(settings.admin_username, settings.admin_password).json()["token"]
