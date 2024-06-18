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
    path('<int:room_id>/assign-trainer/<int:trainer_id>/', RoomViewSet.as_view({'post': 'assign_trainer'}), name='assign-trainer'),
    path('<int:room_id>/remove-trainer/<int:trainer_id>/', RoomViewSet.as_view({'post': 'remove_trainer'}), name='remove-trainer'),
]