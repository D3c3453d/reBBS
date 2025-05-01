from django.contrib.auth.models import AbstractUser
from django.db import models


class GenericModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(GenericModel, AbstractUser):
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    online_status = models.BooleanField(default=False)

    date_joined = None

    @property
    def date_joined(self):
        raise AttributeError("'Member' object has no attribute 'date_joined'")


class Chat(GenericModel):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(Member, through="db.MemberChat", related_name="chats")

    def __str__(self):
        return self.name


class MemberChat(GenericModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("member", "chat")
