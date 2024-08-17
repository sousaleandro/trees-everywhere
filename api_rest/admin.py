from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Plant, PlantedTree

# Activate accounts action
def activate_accounts(modeladmin, request, queryset):
    queryset.update(active=True)

activate_accounts.description = 'Activate account'

# Deactivate accounts action
def deactivate_accounts(modeladmin, request, queryset):
    queryset.update(active=False)

deactivate_accounts.description = 'Deactivate account'

# Needed to show accounts in user admin page
class AccountInline(admin.TabularInline):
    model = Account.users.through
    extra = 1

# Needed to show all planted tree in each plant type
class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    can_delete = False
    
# Costumization of admin page for accounts
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_editable = ('active',)
    actions = [activate_accounts, deactivate_accounts]

# Costumization of admin page for users
class UserAdmin(UserAdmin):
    inlines = (AccountInline,)

# Costumization of admin page for planted trees
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ('user', 'plant', 'planted_at', 'age', 'account', 'location')

# Costumization of admin page for plants
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')
    inlines = (PlantedTreeInline,)

# Register models and admin pages
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(PlantedTree, PlantedTreeAdmin)
admin.site.site_header = 'Trees Everywhere Admin'