import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from ... import models


@pytest.fixture
def admin_user(db):
    return mixer.blend(User, is_staff=True, is_superuser=True)

@pytest.fixture
def sample_category_data():
    return {
        "category_name": "Test Category",
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }

@pytest.fixture
def sample_policy_data():
    return {
        "category": mixer.blend(models.Category).id,
        "policy_name": "Test Policy",
        "sum_assurance": 10000,
        "premium": 500,
        "tenure": 12,
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }