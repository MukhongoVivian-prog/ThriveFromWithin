from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register('meditations', MeditationViewSet)
router.register('breathing-exercises', BreathingExerciseViewSet)
router.register('quotes', MotivationalQuoteViewSet)
router.register('journal-entries', PrivateJournalEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
