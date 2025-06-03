from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet, GroupTherapySessionViewSet, GroupSessionParticipantViewSet

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'group_sessions', GroupTherapySessionViewSet)
router.register(r'group_participants', GroupSessionParticipantViewSet)

urlpatterns = router.urls
