from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('', RoomViewSet)
router.register('(?P<room_pk>\d+)/groups', GroupViewSet, basename='group')
router.register('statute', StatueViewset)
router.register('statute_acceptances', StatueAcceprtanceViewset)


urlpatterns = [
    path('', include(router.urls)),
]