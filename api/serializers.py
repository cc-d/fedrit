from django_typomatic import ts_interface, get_ts
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, PlatformUser


@ts_interface()
class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data):



class LoginUserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')



