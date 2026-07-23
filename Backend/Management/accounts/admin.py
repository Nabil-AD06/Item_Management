from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "full_name",
        "email",
        "department",
        "created_at",
    )

    search_fields = (
        "username",
        "full_name",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )