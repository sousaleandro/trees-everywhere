from django.db import models
from django.contrib.auth.models import AbstractUser

# User model with profile informations such as about and joined
class User(AbstractUser):
    about = models.TextField(blank=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Username: {self.username}'

# Account model with name, created date, active status and relationship with users
class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name='accounts', blank=True)

    def __str__(self):
        return f'Account: {self.name} - Active: {self.active}'

#
class Plant(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Plant: {self.name} - Scientific name: {self.scientific_name}'