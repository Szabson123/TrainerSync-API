from rest_framework import serializers
from .models import *
from users.serializers import *

    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'room', 'created_date', 'update_date']
        
        
class RoomSerializer(serializers.ModelSerializer):
    groups_to_room = GroupSerializer(many=True, read_only=True, source='groups_in_room')
    class Meta:
        model = Room
        fields = ['id', 'name', 'owner', 'is_active', 'created_date', 'update_date', 'groups_to_room']
        
        
class ActivityRoomSerializer(serializers.ModelSerializer):
    unique_users = serializers.SerializerMethodField()
    class Meta:
        model = ActivityClass
        fields = ['id', 'name', 'room', 'groups', 'unique_users']
        
    def get_unique_users(self, obj):
        # users in activity class
        users = set(obj.users.all())
        subusers = set(obj.users.all())
        
        # users in groups in activity_class
        for group in obj.group.all():
            users.update(group.users.all())
            subusers.update(group.subusers.all())
        
        unique_users = list(users)
        unique_subusers = list(subusers)
        
        
        return {
            'users': UserSerializer(unique_users, many=True).data,
            'subusers': SubUserSerializer(unique_subusers, many=True).data,
        }
        

