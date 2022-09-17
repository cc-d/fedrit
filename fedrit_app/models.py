from django.db import models
from django.contrib.auth.models import User

class SiteUser(User):
    class Meta:
        proxy = True

class Sub(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    text = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)

class PGP(models.Model):
    key_type = models.TextField(default='RSA')
    key_length = models.IntegerField(default=4096)
    name_real = models.TextField()
    name_comment = models.TextField()
    name_email = models.TextField()
