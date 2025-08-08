# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobPost


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(JobPost)
