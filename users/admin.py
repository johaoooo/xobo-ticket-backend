from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_per_page = 20
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Xobo Ticket', {
            'fields': ('role', 'prenom', 'avatar'),
            'classes': ('wide',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Xobo Ticket', {
            'fields': ('role', 'prenom'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
