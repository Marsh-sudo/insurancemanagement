import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from insurance import models as CMODEL
from ..views.policy import apply_policy_view, apply_view, history_view

@pytest.fixture
def logged_in_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def client(logged_in_user):
    client = RequestFactory().get(reverse('apply-policy'))
    client.user = logged_in_user
    return client

@pytest.mark.django_db
def test_apply_view(client):
    with pytest.raises(TypeError):
        policy = CMODEL.Policy.objects.create(description='Test Description')
        response = apply_view(client, pk=policy.id)
        assert response.status_code == 302
    # Add more assertions as needed

@pytest.mark.django_db
def test_history_view(client):
    response = history_view(client)
    assert response.status_code == 200
    assertTemplateUsed(response, "customer/history.html")
    # Add more assertions as needed
