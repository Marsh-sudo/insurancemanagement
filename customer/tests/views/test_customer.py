
import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.test import TestCase,Client
from django.urls import reverse


@pytest.mark.django_db
def test_customer_signup_view(client, customer_group, customer_form_data):
    response = client.post(reverse('customersignup'), data=customer_form_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert User.objects.filter(username='testuser').exists()
    assert customer_group.user_set.filter(username='testuser').exists()


class TestFirstView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_GET(self):
        response = self.client.get('customerclick')
        print(response)
        self.assertEqual(response.status_code,200)


class SignUpPageTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.address = 'testuser@email.com'
        self.password = 'password'

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('customersignup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='customer/customersignup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('customersignup'), data={
            'username': self.username,
            'address': self.address,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)


class TestDashboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('customer-dashboard')
        self.user = User.objects.create(username='testuser',password='password')
        self.client.login(username='testuser',password='password')

    def test_dashboard_GET(self,client):
        User.objects.create_user(username="janedoe", password="password")
        self.client.login(username="janedoe", password="password")

        response = client.get(reverse("customer-dashboard"))

        assert response.status_code == 200
        assert response.context["user"].is_authenticated
        # response = self.client.get(self.dashboard_url)
        # self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, template_name='customer/customer_dashboard.html')

    def test_dashboard_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
