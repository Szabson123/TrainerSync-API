from rest_framework import viewsets, status, permissions
from .models import CustomUser, SubUser
from .serializers import UserSerializer, SubUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['PATCH'])
    def change_to_trainer(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        if request.user.is_manager:
            user.is_trainer = True
            user.save()
            return Response({'status': 'user promoted to trainer'}, status=status.HTTP_200_OK)
        return Response({'error': 'somethink went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def change_to_manager(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        if request.user.is_superuser:
            user.is_manager = True
            user.save()
            return Response({'status': 'User promoted to manager'}, status=status.HTTP_200_OK)
        return Response({'error': 'somethink went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class SubUserViewSet(viewsets.ModelViewSet):
    queryset = SubUser.objects.all()
    serializer_class = SubUserSerializer
    
    @action(detail=True, methods=['POST'])
    def create_sub_user(self, request, pk=None):
        main_user = get_object_or_404(CustomUser, pk=pk)
        data = request.data
        data['parent'] = main_user.pk
        serializer = SubUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)