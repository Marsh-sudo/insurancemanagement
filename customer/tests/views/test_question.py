import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from pytest_django.asserts import assertTemplateUsed
from insurance import models as CMODEL
from insurance import forms as CFORM
from customer.models import Customer
from django.test import TestCase,Client
from ...views.policy import apply_view, history_view


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


@pytest.mark.django_db
def test_history_view(client):
    response = history_view(logged_in_user)
    assert response.status_code == 302
    assertTemplateUsed(response, "customer/history.html")



class TestQuestions(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_question_url = reverse('ask-question')
        self.user = User.objects.create(username='testuser',password='password')
        self.client.login(username='testuser',password='password')
        question_item = CMODEL.Question.objects.create(
            user = self.user,
            description = "Question test",
        )

    def test_add_question(self):
        response = self.client.post(self.add_question_url, {
            "description": "Question test",
            "user":self.user.id
        })
        self.assertEqual(response.status_code,302)


def test_question_list(auth_client):
    """Test question list view."""
    response = auth_client.get("ask-question")
    assert response.status_code == 200