from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="Thrive From Within API",
      default_version='v1',
      description="API docs for Thrive platform",
   ),
   public=True,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/mental/', include('mental_health.urls')),
    path('api/learning/', include('learning.urls')),
    path('api/community/', include('community.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/SafeRoom/', include('SafeRoom.urls')),
    path('api/wellness/', include('wellness.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
