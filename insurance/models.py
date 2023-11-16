from customer.models import Customer
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Category Model"""
    category_name = models.CharField(max_length=20)
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name


class Policy(models.Model):
    """Policy Model"""
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    policy_name = models.CharField(max_length=200)
    sum_assurance = models.PositiveIntegerField()
    premium = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField()
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.policy_name


class PolicyRecord(models.Model):
    """Policy Record Model"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="Pending")
    creation_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.policy


class Question(models.Model):
    """Question Model"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    admin_comment = models.CharField(max_length=200, default="Nothing")
    asked_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.description
