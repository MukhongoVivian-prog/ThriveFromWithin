from rest_framework.routers import DefaultRouter
from .views import WellnessProgramViewSet, WellnessEnrollmentViewSet

router = DefaultRouter()
router.register('programs', WellnessProgramViewSet)
router.register('enrollments', WellnessEnrollmentViewSet)

urlpatterns = router.urls
