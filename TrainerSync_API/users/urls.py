from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SubUserViewSet

router = DefaultRouter()
router.register('', UserViewSet)
router.register('(?P<parent_pk>\d+)/subusers', SubUserViewSet, basename='subuser')

urlpatterns = [
    path('', include(router.urls)),
]