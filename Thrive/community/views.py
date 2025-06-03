from rest_framework import viewsets, permissions
from .models import ChatRoom, Message, GroupTherapySession, GroupSessionParticipant
from .serializers import ChatRoomSerializer, MessageSerializer, GroupTherapySessionSerializer, GroupSessionParticipantSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GroupTherapySessionViewSet(viewsets.ModelViewSet):
    queryset = GroupTherapySession.objects.all().order_by('scheduled_for')
    serializer_class = GroupTherapySessionSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupSessionParticipantViewSet(viewsets.ModelViewSet):
    queryset = GroupSessionParticipant.objects.all()
    serializer_class = GroupSessionParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
