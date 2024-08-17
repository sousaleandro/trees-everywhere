from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.userLogin, name="login"),
    # path("planted_trees/", views.get_planted_trees, name="planted_trees"),
]
