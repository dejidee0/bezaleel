from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Display these fields in the admin panel list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_verified', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')

    # Fields shown when viewing a user in the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'bio', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address', 'profile_picture', 'bio', 'is_verified')}
        ),
    )

    ordering = ('email',)

