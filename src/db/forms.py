from django.contrib.auth.forms import AdminUserCreationForm, UserChangeForm

from src.db.models import Member


class MemberCreationForm(AdminUserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "email")


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ("username", "email", "profile_picture", "online_status")
