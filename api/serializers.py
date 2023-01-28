from django_typomatic import ts_interface, get_ts
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import (
    User, PlatformUser, Platform
)
from .utils import valid_name, valid_url
from ..fedrit.settings import HOST_PLATFORM

import logging
logger = logging.getLogger(__name__)


@ts_interface()
class PlatformUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'username', 'password', 'token', 'platform')
        extra_kwargs = {
            'password': {'write_only': True},
            'uuid': {'required': False},
            'platform': {'required': False},
            'uuid': {'required': False, 'read_only': True}
        }

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        platform = data.get('platform', Platform.host_platform.name)

        if not username or not password:
            raise serializers.ValidationError('missing username or password')
        elif not valid_name(username, 'username') or \
            not valid_name(platform):
            raise serializers.ValidationError('invalid platform or username')
        elif password is not None and len(str(password)) < 8:
            raise serializers.ValidationError('password too short')
        
        platform = Platform.objects.filter(name__iexact=platform).distinct()
        if not platform.exists():
            raise serializers.ValidationError('platform does not exist')
        else:
            data['platform'] = platform.first().name

        return data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        platform = validated_data['platform']
        platform = Platform.objects \
            .filter(name__iexact=platform) \
            .distinct().first()

        user = get_user_model().objects.create_user(
            username=username, password=password, platform=platform)
        return user



