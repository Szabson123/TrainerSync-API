from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    @action(detail=True, methods=['POST'])
    def upgrade_to_trainer(self, request, pk=None):
        room = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        
        if user in room.users.all() and room.owner == request.user:
            print(True)
            room.users.remove(user)
            room.trainers.add(user)
            room.save()

            return Response({'status': 'User upgradeed to trainer'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'Somethink went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def remove_trainer(self, request, pk=None):
        room = self.get_object()
        user_id = request.data.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        
        if user in room.trainers.all() and room.owner == request.user:
            room.trainers.remove(user)
            room.users.add(user)
            room.save()
            
            return Response({'status': 'Trainer removed'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'Somethink went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    
class GroupViewSets(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

class AtivityRoomViewSet(viewsets.ModelViewSet):
    queryset = ActivityClass.objects.all()
    serializer_class = ActivityClassSerializer