from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_fields = ['user', 'created_at']
    search_fields = ['user__username', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List all journal entries",
        responses={200: JournalEntrySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new journal entry",
        request_body=JournalEntrySerializer,
        responses={201: JournalEntrySerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a journal entry by ID",
        responses={200: JournalEntrySerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a journal entry by ID",
        request_body=JournalEntrySerializer,
        responses={200: JournalEntrySerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a journal entry by ID",
        request_body=JournalEntrySerializer,
        responses={200: JournalEntrySerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a journal entry by ID",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class TherapistSessionViewSet(viewsets.ModelViewSet):
    queryset = TherapistSession.objects.all()
    serializer_class = TherapistSessionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List all therapist sessions",
        responses={200: TherapistSessionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new therapist session",
        request_body=TherapistSessionSerializer,
        responses={201: TherapistSessionSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a therapist session by ID",
        responses={200: TherapistSessionSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a therapist session by ID",
        request_body=TherapistSessionSerializer,
        responses={200: TherapistSessionSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a therapist session by ID",
        request_body=TherapistSessionSerializer,
        responses={200: TherapistSessionSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a therapist session by ID",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class SendTherapistSessionMessage(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get all previous chat messages for therapist or client",
        responses={200: TherapistSessionSerializer(many=True)}
    )
    def get(self,request,format=None):

        # get all previous chat Messages
        if request.user.role == "therapist":
            data = TherapistSession.objects.filter(therapist=request.user)
        else:
            data = TherapistSession.objects.filter(user=request.user)

        return Response(
            TherapistSessionSerializer(data, many=True, context={"is_therapsit":request.user.role == "therapist"})
        )

    @swagger_auto_schema(
        operation_summary="Send a message in a therapist session",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reciever': openapi.Schema(type=openapi.TYPE_INTEGER, description='Recipient user ID'),
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message content'),
            }
        ),
        responses={200: openapi.Response('Message sent', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'msg': openapi.Schema(type=openapi.TYPE_STRING)
        })), 400: 'Bad Request'}
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