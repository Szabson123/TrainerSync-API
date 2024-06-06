from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('rooms', RoomViewSet)
router.register('groups', GroupViewSets)
router.register('activity_class', AtivityRoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]