import pytest
from insurance.models import PolicyRecord, Question


@pytest.mark.django_db
def test_category_str(create_category):
    category = create_category(category_name="TestCategory")
    assert str(category) == "TestCategory"

@pytest.mark.django_db
def test_policy_str(create_policy):
    policy = create_policy(policy_name="TestPolicy")
    assert str(policy) == "TestPolicy"


@pytest.mark.django_db
def test_question_str(create_customer):
    customer = create_customer(username="testuser2")
    question = Question.objects.create(customer=customer, description="TestQuestion")
    assert str(question) == "TestQuestion"