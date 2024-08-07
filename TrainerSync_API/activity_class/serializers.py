from rest_framework import serializers
from .models import *
from rooms.models import *
from users.serializers import *
from rooms.serializers import *
from drf_spectacular.utils import extend_schema_field
from typing import List, Dict, Any


def format_errors(serializer_errors):
    errors = []
    for field, messages in serializer_errors.items():
        if isinstance(messages, list):
            errors.append(f"{messages[0]}")
        else:
            errors.append(f"{messages}")

    error_message = " ".join(errors)
    return {'error': error_message}


class ActivityClassSerializer(serializers.ModelSerializer):
    unique_users = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=False, write_only=True)
    users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False, write_only=True)
    subusers = serializers.PrimaryKeyRelatedField(queryset=SubUser.objects.all(), many=True, required=False, write_only=True)
    groups_name = serializers.SerializerMethodField()

    class Meta:
        model = ActivityClass
        fields = ['id', 'name', 'groups', 'groups_name', 'unique_users', 'users', 'subusers', 'cost', 'start_date', 'time', 'localization', 'type']

    @extend_schema_field(Dict[str, List[Dict[str, str]]])
    def get_unique_users(self, obj) -> Dict[str, List[Dict[str, str]]]:
        users_in_activity = set(obj.users.all())
        subusers_in_activity = set(obj.subusers.all())

        for group in obj.groups.all():
            users_in_activity.update(group.users.all())
            subusers_in_activity.update(group.subusers.all())

        return {
            'users': [{'first_name': user.first_name, 'last_name': user.last_name} for user in users_in_activity],
            'subusers': [{'first_name': subuser.name, 'last_name': subuser.last_name} for subuser in subusers_in_activity]
        }
    
    @extend_schema_field(List[str])
    def get_groups_name(self, obj) -> List[str]:
        return [group.name for group in obj.groups.all()]
    
    def create(self, validated_data: Dict[str, Any]) -> ActivityClass:
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
        activity_class.create_attendance()
        
        return activity_class


class BalanceForActivityClassSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    room_name = serializers.CharField(source='room.name', read_only=True)
    activity_class_name = serializers.CharField(source='activity_class.name', read_only=True)
    
    class Meta:
        model = BalanceForActivityClass
        fields = ['user_name', 'room_name', 'activity_class', 'activity_class_name', 'amount_due', 'amount_paid', 'paid', 'date']
    
    def get_user_name(self, obj) -> str:
        if obj.user is not None:
            return obj.user.get_full_name()
        elif obj.subuser is not None:
            return f'{obj.subuser.name} rodzic {obj.subuser.parent.get_full_name()}'
        return None

        
class AttendanceForActivityClassSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    room_name = serializers.CharField(source='room.name', read_only=True)
    activity_class_name = serializers.CharField(source='activity_class.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['user_name', 'room_name', 'activity_class', 'activity_class_name', 'present']
        extra_kwargs = {
                'activity_class': {'write_only': True}
        }
    
    def get_user_name(self, obj) -> str:
        if obj.user is not None:
            return obj.user.get_full_name()
        elif obj.subuser is not None:
            return f'{obj.subuser.name} rodzic {obj.subuser.parent.get_full_name()}'
        return None
