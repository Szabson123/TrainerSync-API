from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('(?P<room_pk>\d+)/activities', ActivityClassViewSet),
router.register('(?P<room_pk>\d+)/balance_for_activity', BalanceForActivityClassViewSet),
router.register('(?P<room_pk>\d+)/attendance', AttendanceForActivityClassViewSet),

urlpatterns = [
    path('', include(router.urls)),
]