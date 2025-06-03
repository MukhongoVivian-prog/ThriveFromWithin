from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .models import Meditation, BreathingExercise, MotivationalQuote, PrivateJournalEntry
from .serializers import *

class MeditationViewSet(viewsets.ModelViewSet):
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer
    permission_classes = [IsAuthenticated]


class BreathingExerciseViewSet(viewsets.ModelViewSet):
    queryset = BreathingExercise.objects.all()
    serializer_class = BreathingExerciseSerializer
    permission_classes = [IsAuthenticated]


class MotivationalQuoteViewSet(viewsets.ModelViewSet):
    queryset = MotivationalQuote.objects.all()
    serializer_class = MotivationalQuoteSerializer
    permission_classes = [IsAuthenticated]


class PrivateJournalEntryViewSet(viewsets.ModelViewSet):
    queryset = PrivateJournalEntry.objects.all()
    serializer_class = PrivateJournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
