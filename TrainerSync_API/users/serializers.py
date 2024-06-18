from rest_framework import serializers
from .models import CustomUser, SubUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


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
        fields = ['id', 'username', 'phone_number', 'first_name', 'last_name', 'email', 'sub_user']

class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone_number', 'first_name', 'last_name', 'email', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
