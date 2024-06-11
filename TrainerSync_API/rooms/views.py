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
        
        if user in room.users.all():
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
        
        # ADD if manager
        
        if user in room.trainers.all():
            room.trainers.remove(user)
            room.users.add(user)
            room.save()
            
            return Response({'status': 'Trainer removed'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'Somethink went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'])
    def users_trainers_subusers_list(self, request, pk=None):
        room = self.get_object()
        users = room.users.all()
        subusers = room.subusers.all()
        trainers = room.trainers.all()
        
        users_serializer = SimpleUserSerializer(users, many=True)
        subusers_serializer = SimpleSubUserSerializer(subusers, many=True)
        trainers_serializer = SimpleUserSerializer(trainers, many=True)
        
        return Response({
            'trainers': trainers_serializer.data,
            'users': users_serializer.data,
            'subusers': subusers_serializer.data
        }, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['post'])
    def generate_code(self, request, pk=None):
        room = self.get_object()
        if hasattr(room, 'invitation_code'):
            room.invitation_code.delete()
        # Generowanie nowego kodu
        new_code = room.generate_code()
        invitation_code = InvitationCode.objects.create(room=room, code=new_code)
        serializer = InvitationCodeSerializer(invitation_code)
        return Response({'code': serializer.data}, status=status.HTTP_201_CREATED)

        
    
    
class GroupViewSets(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

    

class StatueViewset(viewsets.ModelViewSet):
    queryset = Statute.objects.all()
    serializer_class = StatueSerializer
    

class StatueAcceprtanceViewset(viewsets.ModelViewSet):
    queryset = StatuteAcceptance.objects.all()
    serializer_class = StatueAcceptanceSerializer
    
    @action(detail=False, methods=['POST'])
    def accept(self, request):
        user = request.user
        statute_id = request.data.get('statute_id')
        statute = get_object_or_404(Statute, pk=statute_id)
        
        acceptance, created = StatuteAcceptance.objects.get_or_create(user=user, statute=statute)
        
        if created:
            return Response({'status': 'Regulamin został zaakceptowany'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Regulamin był już zaakceptowany'}, status=status.HTTP_200_OK)
        