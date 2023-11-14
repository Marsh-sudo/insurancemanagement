# test_views.py

import pytest
from django.test import RequestFactory
from django.urls import reverse

# from mixer.backend.django import mixer
from .. import views


@pytest.mark.django_db
def test_admin_category_view(client):
    response = client.get(reverse('admin-category'))
    assert response.status_code == 200
    assert b"insurance/admin_category.html" in response.content

@pytest.mark.django_db
def test_admin_add_category_view(client, sample_category_data):
    response = client.post(reverse('admin-add-category'), data=sample_category_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert views.models.Category.objects.filter(name='Sample Category').exists()

@pytest.mark.django_db
def test_admin_view_category_view(client, sample_category):
    response = client.get(reverse('admin-view-category'))
    assert response.status_code == 200
    assert sample_category.name.encode() in response.content

@pytest.mark.django_db
def test_admin_delete_category_view(client, sample_category):
    response = client.get(reverse('admin-delete-category'))
    assert response.status_code == 200
    assert sample_category.name.encode() in response.content

@pytest.mark.django_db
def test_delete_category_view(client, sample_category):
    response = client.post(reverse('delete-category', args=[sample_category.pk]))
    assert response.status_code == 302  # Redirect status code after successful deletion
    assert not views.models.Category.objects.filter(pk=sample_category.pk).exists()

@pytest.mark.django_db
def test_admin_update_category_view(client, sample_category):
    response = client.get(reverse('admin-update-category'))
    assert response.status_code == 200
    assert sample_category.name.encode() in response.content

@pytest.mark.django_db
def test_update_category_view(client, sample_category, sample_category_data):
    response = client.post(reverse('update-category', args=[sample_category.pk]), data=sample_category_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert views.models.Category.objects.get(pk=sample_category.pk).name == 'Sample Category'

@pytest.mark.django_db
def test_update_category_view_requires_login():
    factory = RequestFactory()
    request = factory.get(reverse('update-category', args=[1]))
    response = views.update_category_view(request, 1)
    assert response.status_code == 302  # Redirect status code for login required
    assert response.url == reverse('adminlogin')
