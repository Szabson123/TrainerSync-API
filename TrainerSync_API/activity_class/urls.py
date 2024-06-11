from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('activity_class', AtivityRoomViewSet)
router.register('balance_per_user', BalanceForActivityClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
]