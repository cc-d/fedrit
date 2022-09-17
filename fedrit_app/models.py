from django.db import models
from django.contrib.auth.models import User
import gnupg
from fedrit import settings

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

    def generate_key(
        self, key_type: str, key_length: str,
        name_real: str, name_comment: str, name_email: str,
        ):
        print('generating: ', key_type, key_length, name_real, name_comment, name_email)

        gpg = gnupg.GPG(gnupghone=settings.GNUPG_DIR)
        
        key_input = gpg.gen_key_input(
            key_type=key_type, key_length=key_length, 
            name_real=name_real, name_comment=name_comment,
            name_email=name_email
        )

        key = gpg.gen_key(key_input)

        print('key: ', key)
