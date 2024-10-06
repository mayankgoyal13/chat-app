# users/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomUser
from rest_framework import exceptions


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        username = validated_token.get('username')
        print(validated_token.get('username'))
        if username is None:
            raise exceptions.AuthenticationFailed('No username in token')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return user
