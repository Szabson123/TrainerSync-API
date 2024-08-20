from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # My paths
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path('users/', include('users.urls')),
    path('rooms/', include('rooms.urls')),
    path('activity_class/', include('activity_class.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)