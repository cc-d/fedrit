import string
from uuid import uuid4
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import (
    AbstractUser, Group, Permission,
)
from django_typomatic import ts_interface, get_ts, generate_ts
from django.utils import timezone
from fedrit.settings import (
    HOST, VALID_NAME_LEN_MAX, VALID_CHARS
)
from rest_framework.authtoken.models import Token
from .utils import SLIT, gen_token_str, logf
from typing import *
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

    name = models.CharField(default=HOST.name, max_length=VALID_NAME_LEN_MAX)
    domain = models.CharField(default=HOST.domain, max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    host = models.BooleanField(default=False, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['host'], condition=models.Q(
                host=True), name='unique_host'),
        ]

    def __repr__(self):
        return f'<Platform {self.name} {self.id}>'

    def __str__(self):
        return f'<Platform {self.name}>'



def goc_host(host_id=True):
    host, created = Platform.objects.get_or_create(host=True)
    if created:
        logger.info(f'host platform did not exist: {host} created')

    if host_id:
        return str(host.id)
    return host



class PlatformUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # original platform attributes
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    origin_username = models.CharField(max_length=VALID_NAME_LEN_MAX)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add these lines to override the groups and user_permissions fields
    groups = models.ManyToManyField(
        Group, related_name="platform_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="platform_user_set", blank=True)

    # ... the rest of your PlatformUser model

    def __repr__(self):
        return (f'<PlatformUser {self.username} {self.id}>')

    def __str__(self):
        return (f'<PlatformUser {self.username}>')


    @classmethod
    def create_user(
        cls, username, password, return_token=False
    ):
        """ creates new PlatformUser assumes validated in serializer """
        if not username or not password:
            raise ValueError('Missing username, password')

        platform = goc_host(host_id=False)
        return_token = True if return_token else False

        origin_username = username.split('@')[0]

        user = cls(
            username=username,
            origin_username=origin_username,
            platform=platform)
        user.set_password(password)
        user.save()

        utoken = Token.objects.create(user=user)
        logger.debug(f'get_or_create create_user utoken {utoken}')

        #ptoken = PlatUserToken.gen_user_token(user=user, platform=platform)
        #logger.info(f'created plattoken for user {user} {platform}: {ptoken}')


        if return_token:
            return (user, utoken)
        return (user,)


class PlatUserToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    platform = models.OneToOneField(
        Platform, default=goc_host, editable=False, on_delete=models.DO_NOTHING)

    user = models.OneToOneField(
        PlatformUser, editable=False, on_delete=models.DO_NOTHING,
        related_name='PlatUserToken')

    # token_urlsafe(32) returns string w/ len 43
    token = models.CharField(
        max_length=47, default=gen_token_str)


    def __repr__(self):
        return f'<PlatUserToken user={self.user} platform={self.platform}>'

    def __str__(self):
        return self.__repr__()


    def gen_user_token(
        user: Optional[SLIT.platformuser] = None,
        platform: Optional[SLIT.platform] = None
    ) -> SLIT.PlatUserToken:
        """_summary_
        Args:
            user (Optional[PlatformUser], optional): _description_. Defaults to None.
            platform (Optional[Platform], optional): _description_. Defaults to None.
        Returns:
            PlatUserToken: _description_
        """
        return PlatUserToken.objects.create(user=user, platform=platform)


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
        Platform, default=goc_host, on_delete=models.CASCADE)
    name = models.CharField(max_length=VALID_NAME_LEN_MAX)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return (f'<Community {self.name} {self.id} ' \
            f'type={self.get_community_type.display()} ' \
            f'platform={self.platform}>')

    def __str__(self):
        return (f'<Community {self.name}@{self.platform}>')

    @property
    def ctype(self):
        return self.community_type


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # post attributes
    author = models.ForeignKey(
        PlatformUser, blank=True, null=True, on_delete=models.DO_NOTHING)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255)
    platform = models.ForeignKey(
        Platform, default=goc_host, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    author = models.ForeignKey(
        PlatformUser, blank=True, null=True, on_delete=models.DO_NOTHING)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, default='')
    platform = models.ForeignKey(
        Platform, default=goc_host, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(
        Post, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)