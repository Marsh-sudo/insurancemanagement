import pytest
from django.contrib.auth.models import Group, User
from mixer.backend.django import mixer

from customer.models import \
    Customer  # Replace 'yourapp' with the actual name of your app


@pytest.fixture
def user_fixture():
    return User.objects.create_user(
        username='testuser',
        password='testpassword',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def customer_fixture(user_fixture):
    return Customer.objects.create(
        user=user_fixture,
        profile_pic='path/to/profile_pic.jpg',
        address='Test Address',
        mobile='1234567890'
    )


@pytest.fixture
def customer_group():
    return Group.objects.create(name="CUSTOMER")

@pytest.fixture
def customer_user(customer_group):
    return mixer.blend(User, groups=[customer_group])

@pytest.fixture
def customer_form_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
        'first_name': 'Test',
        'last_name': 'User',
        'address': 'Test Address',
        'mobile': '1234567890',
        'profile_pic': 'path/to/profile_pic.jpg'
    }

@pytest.fixture
def customer_signup_view_client(customer_user):
    from django.test import Client
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client