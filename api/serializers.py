import re
from django_typomatic import ts_interface, get_ts, generate_ts
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db.models import Q
from django.conf import settings
from rest_framework.serializers import (
    ModelSerializer, CharField, ValidationError)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import (
    PlatformUser, Platform,
    HOSTINFO, Community, Post, Comment,
    PlatUserToken, goc_host
)
from .utils import (
    valid_name, valid_url, valid_uuid, valid_username,
    def_kwargs, modchoice, logf
)


import logging
logger = logging.getLogger(__name__)

@ts_interface()
class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'
        depth = 1


@ts_interface()
class PlatformUserSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    platform = PlatformSerializer(read_only=True)

    class Meta:
        model = PlatformUser
        fields = (
            'id', 'platform', 'origin_username', 'created_at', 'updated_at',
            'username', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'id': {'required': False},
            'origin_username': {'required': False},

            'created_at': {'read_only': True}, 'updated_at': {'read_only': True},
        }
        depth = 1

    @logf()
    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data.get('password', None)
        plat_id = data.get('platform_id', None)

        if not username or not password:
            raise ValidationError('missing username or password')

        if plat_id is None:
            plat = goc_host(return_id=False)
        else:
            plat = Platform.objects.get(pk=plat_id)

        data['platform'] = plat

        if '@' not in username:
            logger.debug(f'no @ in username adding for {username}')
            username = f'{username}@{plat.domain}'

        if not valid_username(username):
            raise ValidationError('invalid username')
        elif password is not None and len(str(password)) < 8:
            raise ValidationError('password too short')

        return data

    @logf()
    def create(self, validated_data, **kwargs):
        username = validated_data['username']
        password = validated_data['password']
        return_token = kwargs.get('return_token', False)

        return PlatformUser.create_user(
            username=username, password=password, return_token=return_token)

@ts_interface()
class CommunitySerializer(ModelSerializer):
    platform = PlatformSerializer()

    class Meta:
        model = Community
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            'id': {'required': False},
            'community_type': {'required': False},
            'name': {'required':False},
            'created_at': {'read_only': True, 'required': False},
            'updated_at': {'read_only': True, 'required': False},
        }

    @logf()
    def validate(self, data):
        print('data',data,'context',self.context)
        cid = self.context.get('community_id', None)
        ctype = data.get('community_type', None)
        cname = data.get('name', None)

        data['platform'] = goc_host(return_id=False)
        if 'name' not in data:
            cname = self.context.get('community_name', None)
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
            else:
                raise ValidationError('invalid community type')
        else:
            raise ValidationError('commid or name required')


        return data

    @logf()
    def create(self, validated_data):
        name = validated_data['name']
        comtype = validated_data['community_type']

        newcom = Community.objects.create(
            name=name, community_type=comtype)
        return newcom


@ts_interface()
class PostSerializer(ModelSerializer):
    author = PlatformUserSerializer()
    community = CommunitySerializer()
    platform = PlatformSerializer()

    class Meta:
        model = Post
        fields = ('id', 'author', 'community', 'platform', 'url',
                  'title', 'text', 'created_at', 'updated_at')
        depth = 1
        extra_kwargs = {
            'id': {'required': False},
            'platform': {'required': False},
            'author': {'required': False},
            'community': {'required': False},
            'community_id': {'write_only': True, 'required': False},
            'community_name': {'write_only': True, 'required': False},
            'text': {'required': False},
            'url': {'required': False},
            'created_at': {'read_only': True, 'required': False},
            'updated_at': {'read_only': True, 'required': False},
        }

    @logf()
    def validate(self, data):
        author = data.get('author')
        title = data.get('title', None)
        text = data.get('text', '')
        cname = self.context.get('community_name', None)
        cid = self.context.get('community_id', None)
        print('reqcontext', data, self.context)

        if len(title) > 255:
            raise ValidationError('title has 2 b shorter than 255')

        if cname is None and cid is None:
            raise ValidationError('must have com id or name')
        else:
            if cid:
                data['community'] = Community.objects.get(pk=cid)
            elif cname:
                data['community'] = Community.objects.filter(
                    name__iexact=cname).first()

        return data


@ts_interface()
class CommentSerializer(ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'community', 'text', 'post',
                'post_id', 'platform', 'created_at', 'updated_at']
        depth = 1
        extra_kwargs = {
            'id': {'required': False},
            'platform': {'required': False},

            'post': {'required': False},
            'post_id': {'required': False},

            'author': {'required': False},
            'community': {'required': False, 'read_only': True},
            'text': {'required': False},

            'created_at': {'read_only': True, 'required': False},
            'updated_at': {'read_only': True, 'required': False},
        }

    @logf()
    def validate(self, data):
        pid = self.context.get('post_id', None)
        try:
            post = Post.objects.get(pk=pid)
            comms = Comment.objects.filter(post=post).all()
            data['post'] = post
            data['comments'] = list(comms)
        except Exception as e:
            raise ValidationError(f'comm valid error {e}')
        return data


@ts_interface()
class PlatUserTokenSerializer(ModelSerializer):
    user = PlatformUserSerializer()
    platform = PlatformSerializer()

    class Meta:
        model = PlatUserToken
        fields = ['id', 'user', 'platform', 'token']
        read_only_fields = ['token']
        depth = 1
        extra_kwargs = {
            'id': {'required': False},
            'platform': {'required': False},
            'user': {'required': False},
            'token': {'read_only': True, 'required': False}
        }

    @logf()
    def validate(self, data):
        data['platform'] = self.context.get('platform', None)
        data['user'] = self.context.get('user', None)
        return data


# Autogen

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