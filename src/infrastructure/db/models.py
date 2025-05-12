# src/infrastructure/db/models.py
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
    description = models.TextField()
    is_group = models.BooleanField(default=False)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, through="db.MemberChat", related_name="chats")

    def __str__(self):
        return self.name


class MemberChat(GenericModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("member", "chat")


class Message(GenericModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Message by {self.member.username} in {self.chat.name}"
