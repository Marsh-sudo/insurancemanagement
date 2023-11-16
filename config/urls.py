from django.contrib import admin
from django.urls import include, path

# from insurance.views import category,constants,customers, policy, questions

urlpatterns = [
    path("admin/", admin.site.urls),
    path("customer/", include("customer.urls")),
    path("", include("insurance.urls")),
   
]
