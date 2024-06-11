from rest_framework import serializers
from .models import *
from rooms.models import *
from users.serializers import *
from rooms.serializers import *


class ActivityClassSerializer(serializers.ModelSerializer):
    unique_users = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = ActivityClass
        fields = ['id', 'name', 'room', 'groups', 'unique_users', 'groups', 'time']
        
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
        

class BalanceForActivityClassSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = BalanceForActivityClass
        fields = ['user_name', 'room_name', 'activity_class', 'amount_due', 'amount_paid', 'paid', 'date']
        
    