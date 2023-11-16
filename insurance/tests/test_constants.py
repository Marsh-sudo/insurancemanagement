import pytest
from django.test import Client


@pytest.fixture
def client() -> Client:
    """Test client fixture."""
    return Client()


def test_home_view(client):
    """Test home view."""
    response = client.get("")
    assert response.status_code == 200


def test_about_view(client):
    """Test about view."""
    response = client.get("aboutus")
    assert response.status_code == 200