# core/views.py
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # 🔐 Make this public
    serializer_class = RegisterSerializer

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
