
import pytest
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

from .. import views


@pytest.mark.django_db
def test_customerclick_view_authenticated_user(customer_user):
    factory = RequestFactory()
    request = factory.get(reverse('customerclick'))
    request.user = customer_user
    response = views.customerclick_view(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response.url == 'afterlogin'


@pytest.mark.django_db
def test_customerclick_view_unauthenticated_user():
    factory = RequestFactory()
    request = factory.get(reverse('customerclick'))
    response = views.customerclick_view(request)
    assert response.status_code == 200
    assert b'customer/customerclick.html' in response.content


@pytest.mark.django_db
def test_customer_signup_view(client, customer_group, customer_form_data):
    response = client.post(reverse('customersignup'), data=customer_form_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert User.objects.filter(username='testuser').exists()
    assert customer_group.user_set.filter(username='testuser').exists()


@pytest.mark.django_db
def test_customer_signup_view_invalid_data(client):
    response = client.post(reverse('customersignup'), data={})
    assert response.status_code == 200
    assert b'customer/customersignup.html' in response.content


@pytest.mark.django_db
def test_customer_dashboard_view(client, customer_user):
    response = client.get(reverse('customer-dashboard'))
    assert response.status_code == 200
    assert b'customer/customer_dashboard.html' in response.content
