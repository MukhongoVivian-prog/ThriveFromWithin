from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MoodCheckInViewSet,
    JournalEntryViewSet,
    WellnessProgramViewSet,
    ProgramEnrollmentViewSet,
    TherapistSessionViewSet
)

router = DefaultRouter()
router.register('mood-checkins', MoodCheckInViewSet)
router.register('journals', JournalEntryViewSet)
router.register('wellness-programs', WellnessProgramViewSet)
router.register('enrollments', ProgramEnrollmentViewSet)
router.register('therapist-sessions', TherapistSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
