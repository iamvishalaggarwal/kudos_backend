from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Organization, User, Kudo


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "is_deleted")
    list_filter = ("is_deleted", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "organization")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "organization", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "organization",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "organization")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


@admin.register(Kudo)
class KudoAdmin(admin.ModelAdmin):
    list_display = ("sender", "recipient", "short_message", "timestamp")
    list_filter = ("timestamp", "sender", "recipient")
    search_fields = ("sender__username", "recipient__username", "message")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message

    short_message.short_description = "Message"
