"""Test fixtures for the dashboard app."""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from insurance.models import Question


@pytest.fixture
def client():
    """Test client."""
    return Client()


@pytest.fixture
def user():
    """Test user."""
    user = User.objects.create_user(
        username="janedoe",
        email="janedoe@example.com",
        password="password",
    )
    user.set_password("password")
    user.save()
    return user


@pytest.fixture
def Question(user):
    """Test lead."""
    query = Question.objects.create(
        name=user,
        description="question asked",
    )
    query.save()
    return query


@pytest.fixture
def auth_client(client, user):
    """Test client with authenticated user."""
    client.login(username=user.username, password="password")
    return client