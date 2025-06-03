from django_filters import rest_framework as filters
from .models import MoodCheckIn, JournalEntry

class MoodCheckInFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()
    user = filters.CharFilter(field_name="user__username", lookup_expr='icontains')

    class Meta:
        model = MoodCheckIn
        fields = ['date', 'mood', 'user']
class JournalEntryFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()
    user = filters.CharFilter(field_name="user__username", lookup_expr='icontains')

    class Meta:
        model = JournalEntry
        fields = ['date', 'user']