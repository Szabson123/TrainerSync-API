from rest_framework import serializers
from .models import CustomUser, SubUser


def format_errors(serializer_errors):
    errors = []
    for field, messages in serializer_errors.items():
        if isinstance(messages, list):
            errors.append(f"{messages[0]}")
        else:
            errors.append(f"{messages}")

    error_message = " ".join(errors)
    return {'error': error_message}


class SubUserSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.first_name', read_only=True)

    class Meta:
        model = SubUser
        fields = ['id', 'parent_name', 'name', 'last_name', 'number', 'email', 'parent', 'logo_img']
        extra_kwargs = {
            'name': {'required': True},
            'last_name': {'required': True},
            'parent': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    sub_user = SubUserSerializer(many=True, read_only=True, source='subuser_set')

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'sub_user', 'phone_number', 'logo_img']
