# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_admin', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin', 'phone_number', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_admin', 'phone_number', 'address')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)