from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from insurance import models as CMODEL

from .. import forms, models


def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("afterlogin")
    return render(request, "customer/customerclick.html")


def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {"userForm": userForm, "customerForm": customerForm}
    if request.method == "POST":
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name="CUSTOMER")
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect("customerlogin")
    return render(request, "customer/customersignup.html", context=mydict)


def is_customer(user):
    return user.groups.filter(name="CUSTOMER").exists()


@login_required(login_url="customerlogin")
def customer_dashboard_view(request):
    """Customer dashboard"""
    dict = {
        "customer": models.Customer.objects.get(user_id=request.user.id),
        "available_policy": CMODEL.Policy.objects.all().count(),
        "applied_policy": CMODEL.PolicyRecord.objects.all()
        .filter(customer=models.Customer.objects.get(user_id=request.user.id))
        .count(),
        "total_category": CMODEL.Category.objects.all().count(),
        "total_question": CMODEL.Question.objects.all()
        .filter(customer=models.Customer.objects.get(user_id=request.user.id))
        .count(),
    }
    return render(request, "customer/customer_dashboard.html", context=dict)
