from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM

class AdminViewCustomerViewTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testadmin', password='testpassword')

        # Create a client and log in the user
        self.client = Client()
        self.client.force_login(self.user)

    def test_admin_view_customer_view(self):
        # Submit a GET request to the admin view customer view
        response = self.client.get(reverse('admin-view-customer'))

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'insurance/admin_view_customer.html')  # Check for the correct template used

        # Add more assertions as needed based on your specific implementation

class UpdateCustomerViewTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testadmin', password='testpassword')

        # Create a customer for testing
        self.customer = CMODEL.Customer.objects.create(user=self.user)

        # Create a client and log in the user
        self.client = Client()
        self.client.force_login(self.user)

    def test_update_customer_view_form_submission(self):
        # Create a dictionary with valid form data
        form_data = {
            'username': 'testadmin',
        }

        # Submit a POST request with the form data to the update customer view
        response = self.client.post(reverse('update-customer', args=[self.customer.id]), data=form_data)

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 200)

        # Check if the customer information is updated in the database
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.user.username, 'testadmin')

    def test_update_customer_view_invalid_form_submission(self):
        # Submit a POST request without any form data to trigger form validation errors
        response = self.client.post(reverse('update-customer', args=[self.customer.id]))

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 200)  # Check for a successful response

        # Check if the customer information is not updated in the database
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.user.username, 'testadmin')

class DeleteCustomerViewTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testadmin', password='testpassword')

        # Create a customer for testing
        self.customer = CMODEL.Customer.objects.create(user=self.user)

        # Create a client and log in the user
        self.client = Client()
        self.client.force_login(self.user)

    def test_delete_customer_view(self):
        # Submit a GET request to the delete customer view
        response = self.client.get(reverse('delete-customer', args=[self.customer.id]))

        # Assertions based on the expected behavior of your function
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect status
        self.assertRedirects(response, 'admin-view-customer')

        # Check if the customer is deleted from the database
        self.assertFalse(CMODEL.Customer.objects.filter(id=self.customer.id).exists())
