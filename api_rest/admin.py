from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# + admin.site.site_header = 'Trees Everywhere Admin'
admin.site.register(User, UserAdmin)
