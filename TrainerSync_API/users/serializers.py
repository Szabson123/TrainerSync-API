from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token


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
        fields = ['id', 'username', 'is_trainer', 'is_manager', 'phone_number', 'first_name', 'last_name', 'email', 'password', 'sub_user']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)  # Create token for the user
        return user
    


        