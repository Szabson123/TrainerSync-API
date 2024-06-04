from rest_framework import viewsets, status
from .models import CustomUser, SubUser
from .serializers import UserSerliazer, SubUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerliazer
    

class SubUserViewSet(viewsets.ModelViewSet):
    queryset = SubUser.objects.all()
    serializer_class = SubUserSerializer
    
    @action(detail=True, methods=['POST'])
    def create_sub_user(self, request, pk=None):
        main_user = get_object_or_404(CustomUser, pk=pk)
        data = request.data
        data['parent'] = main_user.id
        serializer = SubUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)