from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PGPKey(models.Model):
    fingerprint = models.CharField(
        max_length=255, unique=True, primary_key=True)
    pubkey = models.TextField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<PGPKey {self.fingerprint}>'


class GlobalPlatform(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    pgpkey = models.ForeignKey(PGPKey, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<GlobalPlatform domain={self.domain}>'


class GlobalUser(models.Model):
    uuid = models.UUIDField(primary_key=True)

    # original platform attributes
    origin_platform = models.OneToOneField(
        GlobalPlatform, on_delete=models.DO_NOTHING)
    origin_username = models.CharField(max_length=255)

    pgpkey = models.ForeignKey(
        PGPKey, null=True, blank=True, on_delete=models.DO_NOTHING)
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.DO_NOTHING)

    def __repr__(self):
        return f'<GlobalUser {self.id}>'


class Community(models.Model):
    uuid = models.UUIDField(primary_key=True)
    COMMUNITY_TYPES = (
        ('SUB', 'Subreddit'),
        ('IMGBOARD', 'ImageBoard'),
        ('FORUM', 'Forum'),
    )

    community_type = models.CharField(
        max_length=50, choices=COMMUNITY_TYPES, default='SUB')
    platform = models.OneToOneField(GlobalPlatform, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'<Community {self.name} type={self.get_community_type.display()}>'


class CommunityPost(models.Model):
    uuid = models.UUIDField(primary_key=True)

    # post attributes
    author = models.OneToOneField(
        GlobalUser, blank=True, null=True, on_delete=models.DO_NOTHING)
    text = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255)
    platform = models.OneToOneField(
        GlobalPlatform, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
