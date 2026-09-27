import pytest

from config.settings import Settings


@pytest.fixture(scope="session")
def settings():
    return Settings()