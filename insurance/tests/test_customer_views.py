# test_views.py
import pytest
from customer import models as CMODEL
from django.urls import reverse


@pytest.mark.django_db
def test_admin_view_customer_view(client, admin_user, sample_customer):
    response = client.get(reverse('admin-view-customer'))
    assert response.status_code == 200
    assert b'insurance/admin_view_customer.html' in response.content
    assert sample_customer.first_name.encode() in response.content

@pytest.mark.django_db
def test_update_customer_view(client, admin_user, sample_customer, update_customer_data):
    response = client.post(reverse('update-customer', args=[sample_customer.pk]), data=update_customer_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert CMODEL.Customer.objects.get(pk=sample_customer.pk).first_name == 'Updated'

@pytest.mark.django_db
def test_update_customer_view_invalid_data(client, admin_user, sample_customer):
    response = client.post(reverse('update-customer', args=[sample_customer.pk]), data={})
    assert response.status_code == 200
    assert b'insurance/update_customer.html' in response.content

@pytest.mark.django_db
def test_delete_customer_view(client, admin_user, sample_customer):
    response = client.post(reverse('delete-customer', args=[sample_customer.pk]))
    assert response.status_code == 302  # Redirect status code after successful deletion
    assert not CMODEL.Customer.objects.filter(pk=sample_customer.pk).exists()
