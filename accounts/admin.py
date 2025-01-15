from django.contrib import admin
from .models import User, UserProfile                     # Makes the user and User profile admin visible on the admin panel
from django.contrib.auth.admin import UserAdmin           # Make the password uneditable in the admin panel



# Register your models here.

class CustomerUserAdmin(UserAdmin):                                         # Make the password uneditable in the admin panel
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')  # How name is displayed on the admin panel
    ordering = ('-date_joined',)                                              # Trailing comma is essential, this creates the list in a descending order
    filter_horizontal = ()
    list_filter = ()
    fieldsets =()
    

admin.site.register(User, CustomerUserAdmin)              # Makes the user admin visible on the admin panel
admin.site.register(UserProfile)