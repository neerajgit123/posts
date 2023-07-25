from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Posts, Comments


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "profile",
                    "img_preview",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ["email", "name", "first_name", "last_name", "is_staff"]
    search_fields = ("email", "name")
    readonly_fields = ["img_preview"]
    ordering = ("email",)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "title",
        "likes_count",
        "dislikes_count",
        "total_comments",
    ]

    def username(self, obj):
        return obj.user.username


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "post_title"]

    def username(self, obj):
        return obj.user.username

    def post_title(self, obj):
        return obj.post.title
