from rest_framework import viewsets, permissions
from .models import Guide, Webinar, Toolkit
from .serializers import GuideSerializer, WebinarSerializer, ToolkitSerializer

class GuideViewSet(viewsets.ModelViewSet):
    queryset = Guide.objects.all().order_by('-created_at')
    serializer_class = GuideSerializer
    permission_classes = [permissions.IsAuthenticated]

class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.all().order_by('-date')
    serializer_class = WebinarSerializer
    permission_classes = [permissions.IsAuthenticated]

class ToolkitViewSet(viewsets.ModelViewSet):
    queryset = Toolkit.objects.all().order_by('-uploaded_at')
    serializer_class = ToolkitSerializer
    permission_classes = [permissions.IsAuthenticated]
