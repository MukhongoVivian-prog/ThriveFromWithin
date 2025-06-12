from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JournalEntryViewSet,
    TherapistSessionViewSet
)

router = DefaultRouter()
router.register('journals', JournalEntryViewSet)
router.register('therapist-sessions', TherapistSessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
