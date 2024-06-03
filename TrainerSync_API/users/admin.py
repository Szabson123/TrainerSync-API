from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_manager', 'is_trainer', 'phone_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SubUser)
