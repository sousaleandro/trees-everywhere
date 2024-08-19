from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("api_rest.urls"), name="api"),
    path("", lambda request: redirect("login"))
]
