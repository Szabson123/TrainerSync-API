from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets

class AtivityRoomViewSet(viewsets.ModelViewSet):
    queryset = ActivityClass.objects.all()
    serializer_class = ActivityClassSerializer