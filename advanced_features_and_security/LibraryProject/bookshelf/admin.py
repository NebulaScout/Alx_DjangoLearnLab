from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.html import format_html
from .models import Book, CustomUser, UserProfile

class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')

class CustomUserAdmin(UserAdmin):
    """Custom admin for CustomUser model with additional fields"""
    
    # Fields to display in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    
    # Fields that can be used for searching
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Fields that can be used for filtering
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined', 'date_of_birth')
    
    # Ordering of the user list
    ordering = ('username',)
    
    # Define fieldsets to include custom fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define add_fieldsets for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo')
        }),
    )

class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model"""
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

class CustomGroupAdmin(GroupAdmin):
    """Enhanced admin for managing groups with better display"""
    list_display = ('name', 'get_permissions_count')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    @admin.display(description='Permissions Count')
    def get_permissions_count(self, obj):
        """Return the count of permissions for this group"""
        return obj.permissions.count()

# Unregister the default Group admin and register our custom one
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

# Register models with their respective admin classes
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)