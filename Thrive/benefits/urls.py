from rest_framework.routers import DefaultRouter
from .views import BenefitViewSet, BenefitCategoryViewSet

router = DefaultRouter()
router.register(r'benefits', BenefitViewSet)
router.register(r'categories', BenefitCategoryViewSet)

urlpatterns = router.urls
