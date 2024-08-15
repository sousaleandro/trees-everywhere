from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    about = models.TextField(default='No information provided')
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Username: {self.username} - Email: {self.email}'