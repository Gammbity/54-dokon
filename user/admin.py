from django.contrib import admin
from user import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(models.User)
class UserModelAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ['first_name', 'email']
    list_display_links =['first_name', 'email']
    search_fields = ("email", "first_name")
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )