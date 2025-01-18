from django.contrib import admin
from vendor.models import vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')


# Register your models here.
admin.site.register(vendor, VendorAdmin)