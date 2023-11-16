from django.contrib.auth.views import LoginView
from django.urls import path

from .views import policy, questions, views

urlpatterns = [
    path("customerclick", views.customerclick_view, name="customerclick"),
    path("customersignup", views.customer_signup_view, name="customersignup"),
    path(
        "customer-dashboard", views.customer_dashboard_view, name="customer-dashboard"
    ),
    path(
        "customerlogin",
        LoginView.as_view(template_name="insurance/adminlogin.html"),
        name="customerlogin",
    ),
    path("apply-policy", policy.apply_policy_view, name="apply-policy"),
    path("apply/<int:pk>", policy.apply_view, name="apply"),
    path("history", policy.history_view, name="history"),
    path("ask-question", questions.ask_question_view, name="ask-question"),
    path("question-history", questions.question_history_view, name="question-history"),
]
