from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'logo_img')
    list_filter = ('email', 'is_staff', 'is_active',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'phone_number', 'logo_img')}),  
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'logo_img')}  
        ),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SubUser)
