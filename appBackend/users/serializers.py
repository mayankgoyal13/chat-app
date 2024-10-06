# users/serializers.py

from rest_framework import serializers
from .models import CustomUser
import re

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, value):
        if CustomUser.objects(username=value).first():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if CustomUser.objects(email=value).first():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_phone_number(self, value):
        pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not pattern.match(value):
            raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        if CustomUser.objects(phone_number=value).first():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()

class CurrentUserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    is_online = serializers.CharField(read_only=True)