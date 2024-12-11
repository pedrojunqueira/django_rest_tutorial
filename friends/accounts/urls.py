from django.urls import path
from .api import UserRegistrationView, PasswordUpdateView, EmailUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
    path('update-email/', EmailUpdateView.as_view(), name='update-email'),
]