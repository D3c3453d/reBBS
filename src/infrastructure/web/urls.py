"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path

from src.infrastructure.web.views import (
    all_chats_view,
    chat_view,
    create_chat_view,
    signup_view,
    subscribed_chats_view,
    toggle_chat_subscription_view,
    welcome_view,
)

auth_urlpatterns = [
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
    # Password reset
    path("password-reset/", PasswordResetView.as_view(template_name="auth/password_reset.html"), name="password_reset"),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="auth/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(template_name="auth/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome_view, name="welcome"),
    path("all-chats/", all_chats_view, name="all-chats"),
    path("subscribed-chats/", subscribed_chats_view, name="subscribed-chats"),
    path("chats/create/", create_chat_view, name="create_chat"),
    path("chat/<int:chat_id>/", chat_view, name="chat"),
    path("chat/<int:chat_id>/toggle-subscription/", toggle_chat_subscription_view, name="toggle_subscription"),
    path("auth/", include(auth_urlpatterns)),
]
