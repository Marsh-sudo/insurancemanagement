import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from .. import models
from insurance import models
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.fixture
def admin_user(db):
    return mixer.blend(User, is_staff=True, is_superuser=True)

@pytest.fixture
def sample_category_data():
    return {
        "category_name": "Test Category",
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }

@pytest.fixture
def sample_policy_data():
    return {
        "category": mixer.blend(models.Category).id,
        "policy_name": "Test Policy",
        "sum_assurance": 10000,
        "premium": 500,
        "tenure": 12,
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }


@pytest.mark.django_db
def test_admin_add_policy_view(client, admin_user, sample_category_data, sample_policy_data):
    # Create a category to be used in the form
    response_category = client.post(reverse('admin-add-category'), data=sample_category_data)
    assert response_category.status_code == 302

    # Log in the admin user
    client.force_login(admin_user)

    # Get the created category for the policy form
    category_id = models.Category.objects.last().id

    # Create a request with POST data
    request_data = {
        "category": category_id,
        "policy_name": "Test Policy",
        "sum_assurance": 10000,
        "premium": 500,
        "tenure": 12,
        "creation_date": "2023-01-01",  # Replace with an appropriate date
    }

    response = client.post(reverse('admin-add-policy'), data=request_data)
    
    # Assert that the response is a redirect to 'admin-view-policy'
    assert response.status_code == 302
    assert response.url == reverse('admin-view-policy')

    # Assert that the policy was created
    assert models.Policy.objects.filter(policy_name='Test Policy').exists()


class UpdatePolicyViewTest(TestCase):
    def setUp(self):
        # Create a user for testing (you may adjust this as needed)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Create a category for the policy
        self.category = models.Category.objects.create(category_name='TestCategory')

        # Create a policy for testing
        self.policy = models.Policy.objects.create(
            policy_name='TestPolicy',
            sum_assurance=500,
            premium=500,
            tenure=10,
            category=self.category
        )

    def test_update_policy_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Prepare the updated data
        updated_data = {
            'policy_name': 'UpdatedPolicy',
            'sum_assurance': 600,
            'category': self.category.id,
            'premium':700,
            'tenure':80,

            # Add other fields as needed
        }

        # Get the update URL for the specific policy
        update_url = reverse('update-policy', args=[self.policy.id])

        # Simulate a POST request to update the policy
        response = self.client.post(update_url, data=updated_data)

        # Check if the update was successful (you may adjust this based on your redirect logic)
        self.assertRedirects(response, reverse('admin-update-policy'))

        # Retrieve the policy again to check if it was updated in the database
        updated_policy = models.Policy.objects.get(id=self.policy.id)

        self.assertEqual(updated_policy.policy_name, 'UpdatedPolicy')
        self.assertEqual(updated_policy.tenure, 80)
        self.assertEqual(updated_policy.category, self.category)


