import re
from django_typomatic import ts_interface, get_ts, generate_ts
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
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
        fields = ('id', 'platform_id', 'origin_username', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'platform_id': {'required': False},
            'id': {'required': False},
            'origin_username': {'required': False}
        }

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        data['platform_id'] = host_platform().id

        if not username or not password:
            raise serializers.ValidationError('missing username or password')
        elif not valid_name(username, 'username'):
            raise serializers.ValidationError('invalid username')
        elif password is not None and len(str(password)) < 8:
            raise serializers.ValidationError('password too short')

        return data

    def create(self, validated_data, **kwargs):
        username = validated_data['username']
        password = validated_data['password']
        return_token = kwargs.get('return_token', False)

        user = PlatformUser.create_user(
            username=username, password=password, return_token=return_token)
        return user 


def remove_serializer_suffix(typescript_types_str):
    """ removes the ending of Serializer from types.ts str """
    # Use regex to find the pattern "export interface {type_name}Serializer {"
    pattern = r"export interface ([\w]+)Serializer\s*{"
    # Replace the matching pattern with "export interface {type_name} {"
    updated_types = re.sub(
        pattern, r"export interface \1 {", typescript_types_str)
    return updated_types


TYPES_STRING = remove_serializer_suffix(get_ts(camelize=True))
print('TYPES', TYPES_STRING)
with open('frontend/src/types.ts', 'r+') as f:
    f.write(TYPES_STRING)