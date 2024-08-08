from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.models import CustomUser
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer, format_errors

from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: 'Password change successfully',
            400: 'Bad request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(create=extend_schema(exclude=True))
class RegistrationViewSet(viewsets.ViewSet):
    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
    @action(detail=False, methods=['POST'], permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            formatted_errors = format_errors(serializer.errors)
            return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh': {
                        'type': 'string',
                        'description': 'Refresh token',
                    },
                },
                'required': ['refresh'],
            }
        },
        responses={
            205: OpenApiExample(
                'Token successfully blacklisted',
                value={},
            ),
            400: OpenApiExample(
                'Bad request',
                value={'detail': 'Bad request'},
            ),
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class CustomTokenRefreshView(TokenRefreshView):
    pass