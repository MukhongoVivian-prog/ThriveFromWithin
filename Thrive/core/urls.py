# core/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("user", views.ManageUser, basename="user")
router.register('therapist', views.ManageTherapist, basename="therapist")
router.register("material",views.ManageCompanyMaterial, basename="material")

urlpatterns = [
    path('scenes', views.GetScenes.as_view(), name="scenes"),
    path('sounds', views.ManageSounds.as_view(), name="manage-sounds"),
    path('affirmation',views.GetAffirmations.as_view(), name="affirmation"),
    path('user/login/', views.CustomTokenView.as_view(), name='token_obtain_pair'),
    path('user/question/', views.SetUserEnvironmentAndChallenges.as_view(), name="set-questions")
] + router.urls
