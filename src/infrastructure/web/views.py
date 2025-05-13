from asgiref.sync import async_to_sync
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from infrastructure.db.forms import MemberCreationForm
from interface.controllers.chat import ChatController
from usecases.chat import ChatUsecases, CreateChat, IsSubscribed, SubscribeToChat, UnsubscribeFromChat

from src.infrastructure.db.models import Chat, Member
from src.infrastructure.db.repositories.chat import ChatRepository

chat_repo = ChatRepository()
chat_controller = ChatController(
    ChatUsecases(
        create_chat=CreateChat(chat_repo),
        subscribe=SubscribeToChat(chat_repo),
        unsubscribe=UnsubscribeFromChat(chat_repo),
        is_subscribed=IsSubscribed(chat_repo),
    )
)


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
    is_subscribed = async_to_sync(chat_repo.is_subscribed)(request.user.id, chat_id)
    return render(request, "chat.html", {"chat": chat, "is_subscribed": is_subscribed})


@login_required
def all_chats_view(request, *args, **kwargs):
    chats = list(Chat.objects.all())
    return render(request, "chats.html", {"chats": chats, "title": "All Chats"})


@login_required
def subscribed_chats_view(request, *args, **kwargs):
    chats = list(Chat.objects.filter(members=request.user.id))
    return render(request, "chats.html", {"chats": chats, "title": "Subscribed Chats"})


@login_required
def create_chat_view(request):
    if request.method == "POST":
        chat_controller.handle_create_chat(owner_id=request.user.id, payload=request.POST)
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def toggle_chat_subscription_view(request, chat_id):
    async_to_sync(chat_controller.toggle_subscription)(request.user.id, chat_id)
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def chat_info_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    members = chat.members.all()  # ← список участников чата
    return render(request, "chat_info.html", {"chat": chat, "members": members})


@login_required
def member_profile_view(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, "member_profile.html", {"member": member})


@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.bio = request.POST.get("bio")
        user.save()

        messages.success(request, "Your profile was updated successfully.")
        return redirect("edit_profile")

    return render(request, "edit_profile.html", {"user": user})
