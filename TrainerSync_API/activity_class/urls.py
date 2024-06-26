from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('(?P<room_pk>\d+)/activities', ActivityClassViewSet, basename='activityclass')
router.register('(?P<room_pk>\d+)/balance_for_activity', BalanceForActivityClassViewSet, basename='balanceforactivityclass')
router.register('(?P<room_pk>\d+)/attendance/(?P<activity_class_pk>\d+)', AttendanceForActivityClassViewSet, basename='attendanceforactivityclass')

urlpatterns = [
    path('', include(router.urls)),
]