from rest_framework import viewsets, permissions
from .models import WellnessProgram, WellnessEnrollment
from .serializers import WellnessProgramSerializer, WellnessEnrollmentSerializer
from rest_framework.permissions import IsAuthenticated

class WellnessProgramViewSet(viewsets.ModelViewSet):
    queryset = WellnessProgram.objects.all()
    serializer_class = WellnessProgramSerializer
    permission_classes = [IsAuthenticated]

class WellnessEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = WellnessEnrollment.objects.all()
    serializer_class = WellnessEnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
