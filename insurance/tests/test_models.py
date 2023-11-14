
def test_category_str(create_category):
    category = create_category(category_name="Test Category")
    assert str(category) == "Test Category"

def test_policy_str(create_policy):
    policy = create_policy(policy_name="Test Policy")
    assert str(policy) == "Test Policy"

def test_policy_category_relation(create_policy, create_category):
    category = create_category(category_name="Test Category")
    policy = create_policy(category=category)
    assert policy.category == category
