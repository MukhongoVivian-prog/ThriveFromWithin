from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meditation(models.Model):
    title = models.CharField(max_length=100)
    audio_url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class BreathingExercise(models.Model):
    title = models.CharField(max_length=100)
    duration_seconds = models.IntegerField()
    instructions = models.TextField()

    def __str__(self):
        return self.title

class MotivationalQuote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.text[:50]

class PrivateJournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal by {self.user.email} on {self.created_at.date()}"
