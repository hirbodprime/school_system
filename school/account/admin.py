from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id','username', 'email', 'role', 'national_id']

    fieldsets = UserAdmin.fieldsets + (
        (_('Custom Fields'), {
            'fields': ('role', 'national_id', 'bio', 'latitude', 'longitude'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Custom Fields'), {
            'classes': ('wide',),
            'fields': ('role', 'national_id', 'bio', 'latitude', 'longitude'),
        }),
    )
