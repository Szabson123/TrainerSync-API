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
        
        
class ActivityClassSerializer(serializers.ModelSerializer):
    unique_users = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = ActivityClass
        fields = ['id', 'name', 'room', 'groups', 'unique_users', 'groups']
        
    def get_unique_users(self, obj):
        users_in_activity = set(obj.users.all())
        subusers_in_activity = set(obj.subusers.all())

        for group in obj.groups.all():
            users_in_activity.update(group.users.all())
            subusers_in_activity.update(group.subusers.all())

        return {
            'users': [{'first_name': user.first_name, 'last_name': user.last_name} for user in users_in_activity],
            'subusers': [{'first_name': subuser.name, 'last_name': subuser.last_name} for subuser in subusers_in_activity]
        }