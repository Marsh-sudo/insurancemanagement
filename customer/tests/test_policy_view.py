import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from insurance import models as CMODEL  # Import using the provided alias


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def client(user):
    client = Client()
    client.login(username=user.username, password='testpassword')
    return client

def test_apply_policy_view(client, user):
    response = client.get(reverse('apply-policy'))
    assert response.status_code == 200
    assert 'policies' in response.context
    assert 'customer' in response.context
    assert response.context['customer'] == CMODEL.Customer.objects.get(user=user)

def test_apply_view(client, user):
    policy = CMODEL.Policy.objects.create(
        category=CMODEL.Category.objects.create(category_name='TestCategory'),
        policy_name='TestPolicy',
        sum_assurance=1000,
        premium=50,
        tenure=12
    )

    response = client.get(reverse('apply', args=[policy.id]))
    assert response.status_code == 302  # Redirect status code

    # Check that the PolicyRecord was created
    assert CMODEL.PolicyRecord.objects.filter(
        customer=CMODEL.Customer.objects.get(user=user),
        Policy=policy
    ).exists()

def test_history_view(client, user):
    response = client.get(reverse('history'))
    assert response.status_code == 200
    assert 'policies' in response.context
    assert 'customer' in response.context
    assert response.context['customer'] == CMODEL.Customer.objects.get(user=user)
