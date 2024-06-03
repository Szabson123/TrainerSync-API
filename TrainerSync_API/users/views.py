from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerliazer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerliazer