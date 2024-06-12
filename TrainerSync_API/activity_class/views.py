from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action



class ActivityClassViewSet(viewsets.ModelViewSet):
    queryset = ActivityClass.objects.all()
    serializer_class = ActivityClassSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.create_balances()
        return instance

    @action(detail=True, methods=['post'])
    def create_balances(self, request, pk=None):
        activity_class = self.get_object()
        activity_class.create_balances()
        return Response(status=status.HTTP_200_OK)
    

class BalanceForActivityClassViewSet(viewsets.ModelViewSet):
    queryset = BalanceForActivityClass.objects.all()
    serializer_class = BalanceForActivityClassSerializer