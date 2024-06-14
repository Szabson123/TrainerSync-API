from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token),
    path('api_users/', include('users.urls')),
    path('api_rooms/', include('rooms.urls')),
    path('api_activity_class/', include('activity_class.urls')),
]
