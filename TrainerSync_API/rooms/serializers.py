from rest_framework import serializers
from .models import *
from users.serializers import *


class InvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = ['id', 'room', 'code']
        

class LittleInvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = ['code']

    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'room', 'created_date', 'update_date']
        
        
class RoomSerializer(serializers.ModelSerializer):
    groups_to_room = GroupSerializer(many=True, read_only=True, source='groups_in_room')
    code = LittleInvitationCodeSerializer(read_only=True, source='invitation_code')
    class Meta:
        model = Room
        fields = ['id', 'name', 'owner', 'is_active', 'created_date', 'update_date', 'groups_to_room', 'trainers', 'users', 'subusers', 'code']
        
        
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'id']
        

class SimpleSubUserSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.get_full_name', read_only=True)
    class Meta:
        model = SubUser
        fields = ['parent_name', 'name', 'last_name', 'email', 'number', 'id']
        
        
class StatueSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    class Meta:
        model = Statute
        fields = ['id', 'room_name', 'owner_name', 'description']
        
        
class StatueAcceptanceSerializer(serializers.ModelSerializer):
    statute_name = serializers.CharField(source='statute.room.name', read_only=True)
    statute_owner_name = serializers.CharField(source='statute.owner.get_full_name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = StatuteAcceptance
        fields = ['id', 'statute_name', 'user_name', 'statute_owner_name', 'accepted_at']
        read_only_fields=['accepted_at']
        

