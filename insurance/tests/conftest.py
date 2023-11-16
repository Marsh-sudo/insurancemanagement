import pytest
from datetime import date
from django.contrib.auth.models import User
from customer.models import Customer
from insurance.models import Category,Policy,Question

@pytest.fixture
def create_category():
    def _create_category(category_name="Test Category"):
        return Category.objects.create(category_name=category_name)
    return _create_category

@pytest.fixture
def create_customer():
    def _create_customer(username="testuser", password="testpassword"):
        user = User.objects.create_user(username=username, password=password)
        return Customer.objects.create(user=user, address="Test Address", mobile="1234567890")
    return _create_customer

@pytest.fixture
def create_policy(create_category):
    def _create_policy(policy_name="Test Policy", sum_assurance=10000, premium=500, tenure=12):
        category = create_category()
        return Policy.objects.create(category=category, policy_name=policy_name,
                                     sum_assurance=sum_assurance, premium=premium, tenure=tenure)
    return _create_policy

