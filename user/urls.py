from django.urls import path
from user import views

urlpatterns = [
    path("me/", views.MeView.as_view(), name="me"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("registration/bot/", views.RegistrationWithBotView.as_view(), name="registration-bot"),
    path("logout/", views.LogOutView.as_view(), name='logout'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("token/refresh/", views.RefreshTokenView.as_view(), name='token-refresh'),
    path("edit/password/", views.UsernamePasswordEditView.as_view(), name='edit-password'),
]
