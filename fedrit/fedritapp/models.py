from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GPGKey(models.Model):
    fingerprint = models.CharField(max_length=255, unique=True, primary_key=True)
    pubkey = models.TextField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GlobalPlatform(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    gpgkey = models.ForeignKey(GPGKey, null=True, blank=True, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GlobalUser(models.Model):
    id = models.UUIDField(primary_key=True)
    origin_platform = models.OneToOneField(GlobalPlatform)


class PlatformUser(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    platform = models.OneToOneField(GlobalPlatform, on_delete=models.CASCADE)


class Community(models.Model):
    COMMUNITY_TYPES = (
        ('SUB', 'Subreddit'),
        ('IMGBOARD', 'ImageBoard'),
        ('FORUM', 'Forum'),
    )

    community_type = models.CharField(max_length=50, choices=COMMUNITY_TYPES, default='SUB')
    platform = models.OneToOneField(Platform, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommunityBan(models.Model):
    expires = models.DateTimeField(null=True, blank=True, editable=True)
    shadowban = models.BooleanField(default=True, editable=True)
    user = models.OneToOneField(PlatformUser, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class CommunityPost(models.Model):
    author = models.OneToOneField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
