from django.urls import path
from user import views

urlpatterns = [
    path("me/", views.MeView.as_view(), name="me"),
    path("registration/", views.RegistrationView.as_view(), name="registration")
]