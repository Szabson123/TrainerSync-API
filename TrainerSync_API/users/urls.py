from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('', UserViewSet)
router.register('(?P<parent_pk>\d+)/subusers', SubUserViewSet, basename='subuser')


urlpatterns = [
    path('', include(router.urls)),
]