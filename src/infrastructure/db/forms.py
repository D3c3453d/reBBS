from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from src.infrastructure.db.models import Member


class MemberCreationForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ("username", "email", "password1", "password2")


class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ("username", "email", "profile_picture", "online_status")
