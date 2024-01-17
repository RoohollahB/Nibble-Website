from django.contrib import admin
from .models import User, Address


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    list_filter = ['name', 'email', 'is_active']


admin.site.register(User, UserAdmin)
admin.site.register(Address)
