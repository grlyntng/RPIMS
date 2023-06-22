from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username","role","email", "is_staff", "is_active",)
    list_filter = ("username","role","email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username","email", "password","role","branch",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username","email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "role", "branch",
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin) #insert form into admin site