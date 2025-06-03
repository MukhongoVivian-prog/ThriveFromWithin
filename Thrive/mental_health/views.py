from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from .filters import MoodCheckInFilter
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsEmployee , IsAdminUser, IsCompanyManager

from .models import MoodCheckIn, JournalEntry, WellnessProgram, ProgramEnrollment, TherapistSession
from .serializers import (
    MoodCheckInSerializer,   JournalEntrySerializer,
    WellnessProgramSerializer,
    ProgramEnrollmentSerializer,
    TherapistSessionSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class MoodCheckInViewSet(viewsets.ModelViewSet):
    queryset = MoodCheckIn.objects.all()
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated, IsEmployee]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = MoodCheckInFilter
    search_fields = ['user__username', 'mood']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        if self.request.user.role == 'employee':
            # Employees can only see their own mood check-ins
            return MoodCheckIn.objects.filter(user=self.request.user)
        elif self.request.user.role == 'therapist':
            return MoodCheckIn.objects.filter(user__in=self.request.user.assigned_employees.all())
        return MoodCheckIn.objects.none()
class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser | IsCompanyManager | IsEmployee]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = ['user', 'created_at']
    search_fields = ['user__username', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WellnessProgramViewSet(viewsets.ModelViewSet):
    queryset = WellnessProgram.objects.all()
    serializer_class = WellnessProgramSerializer
    permission_classes = [IsAuthenticated, IsEmployee | IsAdminUser | IsCompanyManager]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProgramEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = ProgramEnrollment.objects.all()
    serializer_class = ProgramEnrollmentSerializer
    permission_classes = [IsAuthenticated, IsEmployee ]


class TherapistSessionViewSet(viewsets.ModelViewSet):
    queryset = TherapistSession.objects.all()
    serializer_class = TherapistSessionSerializer
    permission_classes = [IsAuthenticated, IsEmployee | IsAdminUser | IsCompanyManager]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
