from rest_framework import serializers
from .models import CustomUser, SubUser

class SubUserSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.first_name', read_only=True)

    class Meta:
        model = SubUser
        fields = ['id', 'parent_name', 'name', 'last_name', 'number', 'email', 'parent']
        extra_kwargs = {
            'name': {'required': True},
            'last_name': {'required': True},
            'parent': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    sub_user = SubUserSerializer(many=True, read_only=True, source='subuser_set')

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'sub_user']
