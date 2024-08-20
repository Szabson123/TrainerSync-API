from rest_framework import viewsets, status, permissions
from .models import CustomUser, SubUser
from .serializers import UserSerializer, SubUserSerializer, format_errors
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(create=extend_schema(exclude=True))
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubUserViewSet(viewsets.ModelViewSet):
    serializer_class = SubUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        parent_id = self.kwargs['parent_pk']
        return SubUser.objects.filter(parent_id=parent_id)
    
    def create(self, request, parent_pk=None):
        main_user = get_object_or_404(CustomUser, pk=parent_pk)
        
        data = request.data
        data['parent'] = main_user.pk
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        formatted_errors = format_errors(serializer.errors)
        return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)