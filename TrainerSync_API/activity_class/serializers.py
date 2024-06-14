from rest_framework import serializers
from .models import *
from rooms.models import *
from users.serializers import *
from rooms.serializers import *


class ActivityClassSerializer(serializers.ModelSerializer):
    unique_users = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False, write_only=True)
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False, write_only=True)
    subusers = serializers.PrimaryKeyRelatedField(queryset=SubUser.objects.all(), many=True, required=False, write_only=True)
    groups_name = serializers.SerializerMethodField()

    class Meta:
        model = ActivityClass
        fields = ['id', 'name', 'groups', 'groups_name', 'unique_users', 'users', 'subusers', 'cost', 'start_date', 'end_date']

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

    def get_groups_name(self, obj):
        return [group.name for group in obj.groups.all()]
    
    
    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        subusers_data = validated_data.pop('subusers', [])
        groups_data = validated_data.pop('groups', [])
        activity_class = ActivityClass.objects.create(**validated_data)

        if users_data:
            activity_class.users.set(users_data)
        if subusers_data:
            activity_class.subusers.set(subusers_data)
        if groups_data:
            activity_class.groups.set(groups_data)
        
        activity_class.save()
        activity_class.create_balances()
        
        return activity_class



class BalanceForActivityClassSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    room_name = serializers.CharField(source='room.name', read_only=True)
    activity_class_name = serializers.CharField(source='activity_class.name', read_only=True)
    
    class Meta:
        model = BalanceForActivityClass
        fields = ['user_name', 'room_name', 'activity_class', 'activity_class_name', 'amount_due', 'amount_paid', 'paid', 'date']
    
    def get_user_name(self, obj):
        if obj.user is not None:
            return obj.user.get_full_name()
        elif obj.subuser is not None:
            return f'{obj.subuser.name} rodzic {obj.subuser.parent.get_full_name()}'
        return None

        
    