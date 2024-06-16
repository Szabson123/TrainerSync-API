from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('subusers', SubUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]