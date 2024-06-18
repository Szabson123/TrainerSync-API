from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register('', RegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]