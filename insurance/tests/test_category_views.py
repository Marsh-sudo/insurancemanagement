import pytest
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from insurance import views

@pytest.fixture
def sample_category_data():
    return {
        'category_name': 'Sample Category', 
    }

@pytest.fixture
def sample_category():
    return mixer.blend('insurance.Category', category_name='Sample Category') 


@pytest.mark.django_db
def test_admin_update_category_view(client, sample_category):
    response = client.get(reverse('admin-update-category'))
    assert response.status_code == 200
    assert sample_category.category_name.encode() in response.content
