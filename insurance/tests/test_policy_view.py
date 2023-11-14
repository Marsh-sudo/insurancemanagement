import pytest
from django.urls import reverse

from .. import models


@pytest.mark.django_db
def test_admin_policy_view(client, admin_user):
    response = client.get(reverse('admin-policy'))
    assert response.status_code == 200
    assert b'insurance/admin_policy.html' in response.content

@pytest.mark.django_db
def test_admin_add_policy_view(client, admin_user, sample_category_data):
    response = client.post(reverse('admin-add-policy'), data=sample_category_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert models.Policy.objects.filter(policy_name='Test Policy').exists()

@pytest.mark.django_db
def test_admin_view_policy_view(client, admin_user, sample_policy):
    response = client.get(reverse('admin-view-policy'))
    assert response.status_code == 200
    assert sample_policy.policy_name.encode() in response.content

@pytest.mark.django_db
def test_admin_update_policy_view(client, admin_user, sample_policy, update_policy_data):
    response = client.post(reverse('admin-update-policy', args=[sample_policy.pk]), data=update_policy_data)
    assert response.status_code == 302  # Redirect status code after successful form submission
    assert models.Policy.objects.get(pk=sample_policy.pk).policy_name == 'Updated Policy'
    

@pytest.mark.django_db
def test_admin_update_policy_view_invalid_data(client, admin_user, sample_policy):
    response = client.post(reverse('admin-update-policy', args=[sample_policy.pk]), data={})
    assert response.status_code == 200
    assert b'insurance/update_policy.html' in response.content


@pytest.mark.django_db
def test_admin_delete_policy_view(client, admin_user, sample_policy):
    response = client.post(reverse('admin-delete-policy'), data={'pk': sample_policy.pk})
    assert response.status_code == 302  # Redirect status code after successful deletion
    assert not models.Policy.objects.filter(pk=sample_policy.pk).exists()

@pytest.mark.django_db
def test_admin_view_policy_holder_views(client, admin_user, sample_policy_record, sample_approved_policy_record,
                                        sample_disapproved_policy_record, sample_waiting_policy_record):
    views_to_test = [
        ('admin-view-policy-holder', sample_policy_record),
        ('admin-view-approved-policy-holder', sample_approved_policy_record),
        ('admin-view-disapproved-policy-holder', sample_disapproved_policy_record),
        ('admin-view-waiting-policy-holder', sample_waiting_policy_record),
    ]

    for view_name, sample_record in views_to_test:
        response = client.get(reverse(view_name))
        assert response.status_code == 200
        assert sample_record.customer.get_name.encode() in response.content

@pytest.mark.django_db
def test_approve_request_view(client, admin_user, sample_policy_record):
    response = client.post(reverse('approve-request', args=[sample_policy_record.pk]))
    assert response.status_code == 302  # Redirect status code after successful approval
    assert models.PolicyRecord.objects.get(pk=sample_policy_record.pk).status == 'Approved'

@pytest.mark.django_db
def test_disapprove_request_view(client, admin_user, sample_policy_record):
    response = client.post(reverse('reject-request', args=[sample_policy_record.pk]))
    assert response.status_code == 302  # Redirect status code after successful disapproval
    assert models.PolicyRecord.objects.get(pk=sample_policy_record.pk).status == 'Disapproved'
