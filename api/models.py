import string
from uuid import uuid4
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import (
    User, AbstractUser, AbstractBaseUser
)
from django_typomatic import ts_interface, get_ts, generate_ts
from django.utils import timezone
from fedrit.settings import (
    HOST_PLATFORM, VALID_NAME_LEN_MAX, VALID_CHARS
)
from rest_framework.authtoken.models import Token

import logging
logger = logging.getLogger(__name__)


class PGPKey(models.Model):
    fingerprint = models.CharField(max_length=255, primary_key=True)
    pubkey = models.TextField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<PGPKey {self.fingerprint}>'


class Platform(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=VALID_NAME_LEN_MAX)
    domain = models.CharField(max_length=255)

    #pgpkey = models.ForeignKey(
    #    PGPKey, blank=True, null=True, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Platform {self.name} {self.id}>'

    def __str__(self):
        return f'<Platform {self.name}>'

def host_platform() -> Platform:
    print('hosterd platform')
    host = Platform.objects \
        .filter(name=HOST_PLATFORM['name']) \
        .filter(domain=HOST_PLATFORM['domain']) \
        .first()

    if not host:
        host = Platform.objects.create(
            name=HOST_PLATFORM['name'],
            domain=HOST_PLATFORM['domain'])
    return host


class PlatformUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # original platform attributes
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    origin_username = models.CharField(max_length=VALID_NAME_LEN_MAX)

    #pgpkey = models.ForeignKey(
    #    PGPKey, null=True, blank=True, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (f'<PlatformUser {self.username} {self.id}>')

    def __str__(self):
        return (f'<PlatformUser {self.username}>')


    @classmethod
    def create_user(cls, username, password, return_token=False):
        """ creates new PlatformUser assumes validated in serializer """
        if not username or not password:
            raise ValueError('Missing username, password')

        platform = host_platform()
        return_token = True if return_token else False

        origin_username = username
        username = f'{username}@{platform.name}'
        user = cls(
            username=username,
            origin_username=origin_username, 
            platform=platform)
        user.set_password(password)
        user.save()

        utoken = Token.objects.create(user=user)
        if return_token:
            return (user, utoken)
        return (user,)


class Community(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    COMMUNITY_TYPES = (
        ('SUB', 'Subreddit'),
        ('IMGBOARD', 'ImageBoard'),
        ('FORUM', 'Forum'),
    )

    community_type = models.CharField(
        max_length=20, choices=COMMUNITY_TYPES, default='SUB')

    platform = models.ForeignKey(
        Platform, default=host_platform, on_delete=models.CASCADE)
    name = models.CharField(max_length=VALID_NAME_LEN_MAX)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (f'<Community {self.name} {self.id} ' \
            f'type={self.get_community_type.display()} ' \
            f'platform={self.platform}>')

    def __str__(self):
        return (f'<Community {self.name}@{self.platform}>')


class CommunityPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # post attributes
    author = models.OneToOneField(
        PlatformUser, blank=True, null=True, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255)
    platform = models.ForeignKey(
        Platform, default=host_platform, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)