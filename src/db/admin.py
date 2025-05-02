from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from src.db.forms import MemberChangeForm, MemberCreationForm
from src.db.models import Chat, Member, MemberChat


class MemberAdmin(UserAdmin):
    model = Member
    add_form = MemberCreationForm
    form = MemberChangeForm
    add_fieldsets = ((None, {"fields": ("username", "email", "password1", "password2")}),)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "profile_picture")}),
        ("Status", {"fields": ("online_status",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    list_display = ("username", "email", "online_status", "is_staff", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active", "online_status")
    search_fields = ("username", "email")
    readonly_fields = ("created_at", "updated_at", "last_login")
    ordering = ("-created_at",)


class MemberChatInline(admin.TabularInline):
    model = MemberChat
    extra = 1
    raw_id_fields = ("member", "chat")
    readonly_fields = ("created_at",)


class ChatAdmin(admin.ModelAdmin):
    list_display = ("name", "is_group", "created_at", "get_members_count")
    list_filter = ("is_group",)
    search_fields = ("name",)
    inlines = [MemberChatInline]
    readonly_fields = ("created_at", "updated_at")

    def get_members_count(self, obj: Chat):
        return obj.members.count()

    get_members_count.short_description = "Participants"


admin.site.register(Member, MemberAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(MemberChat)
