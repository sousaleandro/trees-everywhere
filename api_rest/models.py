from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    about = models.TextField(default='No information provided')
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Username: {self.username} - Email: {self.email}'

class Account(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Account: {self.name} - Active: {self.active}'
