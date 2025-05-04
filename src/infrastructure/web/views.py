from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def chat_view(request, *args, **kwargs):
    context = {}
    return render(request, "chat.html", context)
