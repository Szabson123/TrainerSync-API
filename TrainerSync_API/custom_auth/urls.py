from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet, CustomTokenObtainPairView, LogoutView, CustomTokenRefreshView, ChangePasswordView

router = DefaultRouter()
router.register('', RegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

]