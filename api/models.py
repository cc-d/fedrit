import string
from uuid import uuid4
from datetime import datetime, timedelta
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import (
    User, AbstractUser, AbstractBaseUser
)
from django_typomatic import ts_interface, get_ts, generate_ts
from django.utils import timezone
from ..fedrit.settings import HOST_PLATFORM
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
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    name = models.CharField(max_length=30, unique=True)
    domain = models.CharField(max_length=255, unique=True)

    pgpkey = models.ForeignKey(
        PGPKey, blank=True, null=True, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<GlobalPlatform domain={self.domain}>'

    @property
    def host_platform(self):
        """ Retrieves current host platform, creates if it does not exist. """
        return Platform.objects.get_or_create(
            name=HOST_PLATFORM['name'], domain=HOST_PLATFORM['domain'])


class PlatformUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # original platform attributes
    platform = models.OneToOneField(
        Platform, default=Platform.host_platform, on_delete=models.CASCADE)

    username = models.CharField(max_length=30)

    pgpkey = models.ForeignKey(
        PGPKey, null=True, blank=True, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (f'<GlobalUser {self.uuid} ' \
            f'username={self.username} platform={self.platform} >')

    def create_user(self, username, password, platform=None):
        """ creates new PlatformUser assumes validated in serializer """
        if not username or not password:
            raise ValueError('Missing username, password')
        if platform is None:
            platform = Platform.host_platform

        user = PlatformUser(username=username, platform=platform)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user



class Community(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    COMMUNITY_TYPES = (
        ('SUB', 'Subreddit'),
        ('IMGBOARD', 'ImageBoard'),
        ('FORUM', 'Forum'),
    )

    community_type = models.CharField(
        max_length=50, choices=COMMUNITY_TYPES, default='SUB')

    platform = models.OneToOneField(Platform, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Community {self.name} type={self.get_community_type.display()}>'


class CommunityPost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # post attributes
    author = models.OneToOneField(
        PlatformUser, blank=True, null=True, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255)
    platform = models.OneToOneField(Platform, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)