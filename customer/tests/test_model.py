# test_models.py

import pytest


@pytest.mark.django_db
def test_customer_model_properties(customer_fixture):
    assert customer_fixture.get_name == 'Test User'
    assert customer_fixture.get_instance == customer_fixture

@pytest.mark.django_db
def test_customer_model_str_method(customer_fixture):
    assert str(customer_fixture) == 'Test'
