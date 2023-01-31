from django_typomatic import ts_interface, get_ts, generate_ts
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import (
    User, PlatformUser, Platform, host_platform
)
from .utils import valid_name, valid_url, valid_uuid
from fedrit.settings import HOST_PLATFORM

import logging
logger = logging.getLogger(__name__)

@ts_interface()
class PlatformUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('uuid', 'platform', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True},
            'platform': {'required': False},
            'uuid': {'required': False}
        }

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        platform = data.get('platform', None)

        if not username or not password:
            raise serializers.ValidationError('missing username or password')
        elif not valid_name(username, 'username'):
            raise serializers.ValidationError('invalid username')
        elif password is not None and len(str(password)) < 8:
            raise serializers.ValidationError('password too short')

        if platform is not None:
            if not valid_uuid(platform):
                raise serializers.ValidationError('invalid platform name')
            try:
                platform = Platform.objects.get(pk=platform)
            except ObjectDoesNotExist:
                raise serializers.ValidationError('platform does not exist')
            data['platform'] = platform.first().uuid
        else:
            platform = host_platform()
            data['platform'] = platform.uuid
        return data

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        platform_name = validated_data['platform']
        platform = Platform.objects \
            .filter(name__iexact=platform) \
            .distinct()

        if platform.exists():
            raise ValueError(f'platform {platform_name} already exists')
        else:
            platform = platform.first()

        user = get_user_model().objects.create_user(
            username=username, password=password, platform=platform)
        return user

generate_ts('frontend/types.ts')
