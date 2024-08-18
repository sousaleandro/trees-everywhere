from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.userLogin, name="login"),
    path("home/", views.home, name="home"),
    path("profile/", views.get_profile, name="profile"),
    path("planted_trees/", views.get_planted_trees, name="planted_trees"),
    path("planted_trees/details/<int:planted_tree_id>/", views.get_planted_tree_details, name="planted_tree_details"),
    path("planted_trees/plant/", views.plant_tree, name="plant_tree"),
    path("api/planted_trees/", views.get_planted_trees_api, name="get_planted_trees_api"),
]
