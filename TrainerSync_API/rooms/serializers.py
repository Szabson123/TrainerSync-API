from rest_framework import serializers
from .models import *
        
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'room', 'created_date', 'update_date']
        
        
class RoomSerializer(serializers.ModelSerializer):
    groups_to_room = GroupSerializer(many=True, read_only=True, source='groups')
    class Meta:
        model = Room
        fields = ['id', 'name', 'owner', 'is_active', 'created_date', 'update_date', 'groups_to_room']