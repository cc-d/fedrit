import re
from django_typomatic import ts_interface, get_ts, generate_ts
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer, CharField, ValidationError)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import (
    User, PlatformUser, Platform, host_platform, Community, Post
)
from .utils import (
    valid_name, valid_url, valid_uuid, valid_username,
    def_kwargs, modchoice
)
from fedrit.settings import HOST_PLATFORM

import logging
logger = logging.getLogger(__name__)

@ts_interface()
class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


@ts_interface()
class PlatformUserSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    platform = PlatformSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'platform', 'origin_username', 'created_at', 'updated_at',
            'username', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'platform': {'read_only': True},
            'id': {'required': False},
            'origin_username': {'required': False},

            'created_at': {'read_only': True}, 'updated_at': {'read_only': True},
        }

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        data['platform'] = host_platform()

        if not username or not password:
            raise ValidationError('missing username or password')
        elif not valid_username(username):
            raise ValidationError('invalid username')
        elif password is not None and len(str(password)) < 8:
            raise ValidationError('password too short')

        return data

    def create(self, validated_data, **kwargs):
        username = validated_data['username']
        password = validated_data['password']
        return_token = kwargs.get('return_token', False)

        user = PlatformUser.create_user(
            username=username, password=password, return_token=return_token)
        return user 


@ts_interface()
class CommunitySerializer(ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'community_type', 'platform',
                  'name', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'required': False},
            'community_type': {'required': False},
            'platform': {'required': False, 'read_only': True},
            'name': {'required': False},
            'created_at': {'read_only': True, 'required': False}, 
            'updated_at': {'read_only': True, 'required': False},
        }

    def validate(self, data):
        cname = data.get('name', None)
        ctype = data.get('community_type', None)
        cid = data.get('id', None)

        data['platform'] = host_platform()

        if cid:
            try:
                comm = Community.objects.get(pk=cid)
                return comm
            except ObjectDoesNotExist as e:
                raise ValidationError('community id does not exist')
        elif cname:
            if not valid_name(cname):
                raise ValidationError('missing or invalid username')

            comm = Community.objects.filter(name=cname).first()
            if comm: return comm

            if ctype:
                ctype = str(ctype).upper()
                if ctype not in [x[0] for x in Community.COMMUNITY_TYPES]:
                    raise ValidationError('invalid community type')

                comm = Community.objects.filter(
                    community_type=ctype, name=cname).first()
                if comm: return comm

                data['community_type'] = ctype
            else: raise ValidationError('invalid community type')
        else: raise ValidationError('commid or name required')


        return data

    def create(self, validated_data):
        name = validated_data['name']
        comtype = validated_data['community_type']

        newcom = Community.objects.create(
            name=name, community_type=comtype)
        return newcom



@ts_interface()
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def validate(self, data):
        title = data.get('title', None)
        text = data.get('text', '')
        cname = data.get('community_name', None)
        cid = data.get('community_id', None)

        if len(title) > 255:
            raise ValidationError('title has 2 b shorter than 255')
        elif cname is None and cid is None:
            raise ValidationError('must have com id or name')
        
        if cname:
            comm = Community.objects.filter(name__iexact=cname).first()
            if comm is None: raise ValidationError('badname')
        elif cid:
            try:
                comm = Community.objects.get(pk=cid)
            except ObjectDoesNotExist as e:
                raise ValidationError('id doesnt exist')

        data['community'] = comm
        return data


LOCALS = dict(locals().items())


def remove_serializer_suffix(ts_types_str: str):
    """ removes the ending of Serializer from types.ts str """
    # class names in this file ending in Serializer
    snames = serializer_names()
    # regex replacement patterns
    patterns = [
        r"(export interface )([a-zA-Z0-9]+)Serializer(\s*{)",
        r"(: )([a-zA-Z0-9]*)Serializer(;)"]

    for p in patterns:
        # Replace the matching pattern with "export interface {type_name} {"
        ts_types_str = re.sub(p, r'\1\2\3', ts_types_str)            
    return ts_types_str


def serializer_names():
    global LOCALS
    litems = list(LOCALS.keys())
    reg = '^[a-zA-Z0-9]*Serializer'
    return [x for x in litems if re.search(reg, x)]


TYPES_STRING = remove_serializer_suffix(get_ts(camelize=True))

print(f'\nAUTOGENERATED TYPES:\n\n{TYPES_STRING}')
with open('frontend/src/types.ts', 'r+') as f:
    f.write(TYPES_STRING)