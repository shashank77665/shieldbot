from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ShieldbotUser

class ShieldbotUserAdmin(UserAdmin):
    """Admin configuration for ShieldbotUser model"""
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')
    
    # Add profile picture to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {'fields': ('profile_picture',)}),
    )

# Register the custom admin class with the model
admin.site.register(ShieldbotUser, ShieldbotUserAdmin) 