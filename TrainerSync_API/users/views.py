from rest_framework import viewsets, status, permissions
from .models import CustomUser, SubUser
from .serializers import UserSerializer, SubUserSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(create=extend_schema(exclude=True))
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method \"POST\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer},)
    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubUserViewSet(viewsets.ModelViewSet):
    queryset = SubUser.objects.all()
    serializer_class = SubUserSerializer
    
    @action(detail=True, methods=['POST'])
    def create_sub_user(self, request, pk=None):
        main_user = get_object_or_404(CustomUser, pk=pk)
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided'}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        data['parent'] = main_user.pk
        serializer = SubUserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
