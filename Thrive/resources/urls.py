from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, ResourceCategoryViewSet

router = DefaultRouter()
router.register(r'resources', ResourceViewSet)
router.register(r'categories', ResourceCategoryViewSet)

urlpatterns = router.urls
