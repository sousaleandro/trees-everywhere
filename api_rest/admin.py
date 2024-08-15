from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Plant

# Activate accounts action
def activate_accounts(modeladmin, request, queryset):
    queryset.update(active=True)

activate_accounts.description = 'Activate account'

# Deactivate accounts action
def deactivate_accounts(modeladmin, request, queryset):
    queryset.update(active=False)

deactivate_accounts.description = 'Deactivate account'

# Costumization of admin page for accounts
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_editable = ('active',)
    actions = [activate_accounts, deactivate_accounts]

# Add accounts to user in admin page
class AccountInline(admin.TabularInline):
    model = Account.users.through
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = (AccountInline,)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Plant)

admin.site.site_header = 'Trees Everywhere Admin'