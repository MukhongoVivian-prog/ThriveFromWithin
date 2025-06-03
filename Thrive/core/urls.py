# core/urls.py

from django.urls import path
from .views import RegisterView, CustomTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenView.as_view(), name='token_obtain_pair'),
]
