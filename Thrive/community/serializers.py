from rest_framework import serializers
from .models import ChatRoom, Message, GroupTherapySession, GroupSessionParticipant

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = ChatRoom
        fields = '__all__'

class GroupTherapySessionSerializer(serializers.ModelSerializer):
    therapist = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GroupTherapySession
        fields = '__all__'

class GroupSessionParticipantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = GroupSessionParticipant
        fields = '__all__'
