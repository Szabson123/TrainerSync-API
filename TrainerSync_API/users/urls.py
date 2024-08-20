from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SubUserViewSet
from django.conf.urls.static import static
from django.conf import settings


router = DefaultRouter()
router.register('', UserViewSet)
router.register('(?P<parent_pk>\d+)/subusers', SubUserViewSet, basename='subuser')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)