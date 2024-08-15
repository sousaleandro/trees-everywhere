from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account

# Add accounts to user in admin page
class AccountInline(admin.TabularInline):
    model = Account.users.through
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline,)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Account)

admin.site.site_header = 'Trees Everywhere Admin'