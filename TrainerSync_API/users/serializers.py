from rest_framework import serializers
from .models import *

class UserSerliazer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'is_trainer', 'is_manager', 'phone_number', 'first_name', 'last_name', 'email', 'password',]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user