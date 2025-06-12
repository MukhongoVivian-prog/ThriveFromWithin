from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import User
from core.permissions import IsEmployee 

from .models import ChatMessage, JournalEntry, TherapistSession
from .serializers import (
    JournalEntrySerializer,
    TherapistSessionSerializer
)

from django.db.models import Q

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
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


class TherapistSessionViewSet(viewsets.ModelViewSet):
    queryset = TherapistSession.objects.all()
    serializer_class = TherapistSessionSerializer
    permission_classes = [IsAuthenticated, IsEmployee | IsAdminUser | IsCompanyManager]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SendTherapistSessionMessage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,format=None):

        # get all previous chat Messages
        if request.user.role == "therapist":
            data = TherapistSession.objects.filter(therapist=request.user)
        else:
            data = TherapistSession.objects.filter(user=request.user)

        return Response(
            TherapistSessionSerializer(data, many=True, context={"is_therapsit":request.user.role == "therapist"})
        )

    def post(self,request,format=None):
        data = request.POST
        sender = request.user
        recipient_id = data['reciever']
        message = data['message']

        try:
            reciever = User.objects.get(id=recipient_id)
            therapist = sender
            client = reciever

            if reciever.role == "therapist":
                client = sender
                therapist = reciever

            try:
                session = TherapistSession.objects.get(Q(user=client)&Q(therapist=therapist))
            except TherapistSession.DoesNotExist:
                session = TherapistSession(
                    user = client,
                    therapist = therapist
                )

                session.save()

                # save chat message
                chat = ChatMessage(
                    session = session,
                    message = message,
                    from_therapist = request.user.role == "therapist"
                )

                chat.save()

                return Response({"msg":"sent"})

        except (User.DoesNotExist, TherapistSession.DoesNotExist):
            return Response(status=400)