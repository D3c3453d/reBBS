from django.shortcuts import redirect, render


def chat_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat.html", context)
