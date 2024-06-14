from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token),
    path('api_users/', include('users.urls')),
    path('api_rooms/', include('rooms.urls')),
    path('api_activity_class/', include('activity_class.urls')),
]
