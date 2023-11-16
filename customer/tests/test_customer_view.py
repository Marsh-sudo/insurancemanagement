
import pytest
from django.contrib.auth.models import User
from django.urls import reverse


# @pytest.mark.django_db
# def test_customerclick_view_authenticated_user(customer_user):
#     factory = RequestFactory()
#     request = factory.get(reverse('customerclick'))
#     request.user = customer_user
#     response = views.customerclick_view(request)
#     assert isinstance(response, HttpResponseRedirect)
#     assert response.url == 'afterlogin'


@pytest.mark.django_db
def test_customer_signup_view(client, customer_group, customer_form_data):
    response = client.post(reverse('customersignup'), data=customer_form_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert User.objects.filter(username='testuser').exists()
    assert customer_group.user_set.filter(username='testuser').exists()

