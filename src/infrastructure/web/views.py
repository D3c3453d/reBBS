from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from infrastructure.db.forms import MemberCreationForm

from src.infrastructure.db.models import Chat


def welcome_view(request, *args, **kwargs):
    return render(request, "welcome.html")


def signup_view(request):
    """
    Render and process the user registration form.
    """
    if request.method == "POST":
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("login")
    else:
        form = MemberCreationForm()

    return render(request, "auth/signup.html", {"form": form})


@login_required
def chat_view(request, chat_id, *args, **kwargs):
    chat = get_object_or_404(Chat, id=chat_id)
    return render(request, "chat.html", {"chat": chat})


@login_required
def all_chats_view(request, *args, **kwargs):
    chats = list(Chat.objects.all())
    return render(request, "chats.html", {"chats": chats, "title": "All Chats"})


@login_required
def subscribed_chats_view(request, *args, **kwargs):
    chats = list(Chat.objects.filter(members=request.user.id))
    return render(request, "chats.html", {"chats": chats, "title": "Subscribed Chats"})
