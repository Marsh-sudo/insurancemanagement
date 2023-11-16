import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from .. import models
from insurance import models


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


@pytest.mark.django_db
def test_admin_add_policy_view(client, admin_user, sample_category_data, sample_policy_data):
    # Create a category to be used in the form
    response_category = client.post(reverse('admin-add-category'), data=sample_category_data)
    assert response_category.status_code == 302

    # Log in the admin user
    client.force_login(admin_user)

    # Get the created category for the policy form
    category_id = models.Category.objects.last().id

    # Create a request with POST data
    request_data = {
        "category": category_id,
        "policy_name": "Test Policy",
        "sum_assurance": 10000,
        "premium": 500,
        "tenure": 12,
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }

    response = client.post(reverse('admin-add-policy'), data=request_data)
    
    # Assert that the response is a redirect to 'admin-view-policy'
    assert response.status_code == 302
    assert response.url == reverse('admin-view-policy')

    # Assert that the policy was created
    assert models.Policy.objects.filter(policy_name='Test Policy').exists()