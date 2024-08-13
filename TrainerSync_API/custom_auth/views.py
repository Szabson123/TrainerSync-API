from django.shortcuts import render
from drf_spectacular.utils import extend_schema, extend_schema_view

from users.models import CustomUser
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, ChangePasswordSerializer, format_errors

from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Konto zostało aktywowane.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Link aktywacyjny jest nieprawidłowy!'}, status=status.HTTP_400_BAD_REQUEST)


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