from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            room_id = view.kwargs.get('room_pk')
            room = get_object_or_404(Room, pk=room_id)
            return room.owner == request.user
        return True


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RoomCreateSerializer
        return RoomSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def assign_trainer(self, request, room_id=None, trainer_id=None):
        room = get_object_or_404(Room, pk=room_id)
        user = get_object_or_404(CustomUser, pk=trainer_id)
        
        if user in room.users.all():
            room.users.remove(user)
            room.trainers.add(user)
            room.save()
            return Response({'status': 'User upgraded to trainer'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    def remove_trainer(self, request, room_id=None, trainer_id=None):
        room = get_object_or_404(Room, pk=room_id)
        user = get_object_or_404(CustomUser, pk=trainer_id)
        
        if room.owner != request.user:
            return Response('You are not the owner of this room', status=status.HTTP_403_FORBIDDEN)
        
        if user in room.trainers.all():
            room.trainers.remove(user)
            room.users.add(user)
            room.save()
            return Response({'status': 'Trainer removed'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    def accepet_user(self, request, room_id=None, unaccepted_id=None):
        room = get_object_or_404(Room, pk=room_id)
        user = get_object_or_404(CustomUser, pk=unaccepted_id)
        
        if room.owner != request.user:
            return Response('You are not the owner of this room', status=status.HTTP_403_FORBIDDEN)
        
        if user in room.unaccepted_users.all():
            room.unaccepted_users.remove(user)
            room.users.add(user)
            room.save()
            return Response({'status': 'User accepted'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    
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
        
    @action(detail=True, methods=['POST'])
    def generate_code(self, request, pk=None):
        room = self.get_object()
        if hasattr(room, 'invitation_code'):
            room.invitation_code.delete()
        new_code = room.generate_code()
        invitation_code = InvitationCode.objects.create(room=room, code=new_code)
        serializer = InvitationCodeSerializer(invitation_code)
        return Response({'code': serializer.data}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['POST'])
    def join(self, request):
        code = request.data.get('code')
        user = self.request.user
        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        invitation_code = get_object_or_404(InvitationCode, code=code)
        room = invitation_code.room

        if user in room.users.all() or user in room.trainers.all() or user in room.unaccepted_users.all():
            return Response({'error': 'User is already in the room'}, status=status.HTTP_400_BAD_REQUEST)
        
        room.unaccepted_users.add(user)
        room.save()

        return Response({'status': 'User added to the room'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def get_my_rooms(self, request):
        user = request.user
        rooms = Room.objects.filter(owner=user)
        serializer = RoomSerializer(rooms, many=True)
        return Response({'rooms': serializer.data}, status=status.HTTP_200_OK)
    
    
class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        room_id = self.kwargs['room_pk']
        return Group.objects.filter(room_id=room_id)

    def perform_create(self, serializer):
        room_id = self.kwargs['room_pk']
        room = get_object_or_404(Room, pk=room_id)

        if room.owner != self.request.user:
            raise PermissionDenied("You do not have permission to add groups to this room.")
        
        serializer.save(room=room)
    

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
        