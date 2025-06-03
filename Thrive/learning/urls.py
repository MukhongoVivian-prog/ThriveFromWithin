from rest_framework.routers import DefaultRouter
from .views import GuideViewSet, WebinarViewSet, ToolkitViewSet

router = DefaultRouter()
router.register(r'guides', GuideViewSet)
router.register(r'webinars', WebinarViewSet)
router.register(r'toolkits', ToolkitViewSet)

urlpatterns = router.urls
# This will automatically generate the necessary URL patterns for the viewsets defined in views.py.
