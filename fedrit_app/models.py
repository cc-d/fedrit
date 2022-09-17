from django.db import models
from django.contrib.auth.models import User
import gnupg
from fedrit import settings
from pathlib import Path

class SiteUser(User):
    class Meta:
        proxy = True

class Sub(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sub<{self.name}>'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    text = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Post<{self.name}>'

class PGP(models.Model):
    id = models.AutoField(primary_key=True)
    key_type = models.TextField(default='RSA')
    key_length = models.IntegerField(default=4096)
    name_real = models.TextField(max_length=50)
    name_comment = models.TextField(max_length=2000)
    name_email = models.TextField(max_length=200)
    fingerprint = models.TextField(null=True, max_length=50)

    def generate_key(self):
        if self.fingerprint is None:
            print('generating: ', self.key_type, self.key_length, self.name_real, self.name_comment, self.name_email)
            print(settings.GNUPG_DIR)
            gpg = gnupg.GPG(gnupghome=Path(settings.GNUPG_DIR))
        
            key_input = gpg.gen_key_input(
                key_type=self.key_type, key_length=self.key_length, 
                name_real=self.name_real, name_comment=self.name_comment,
                name_email=self.name_email
            )

            key = gpg.gen_key(key_input)

            print('generated: ', key_input, str(vars(key)), str(key.fingerprint))

            self.fingerprint = str(key.fingerprint)
            self.save()

    def __str__(self):
        return f'PGP<{self.name_email}>'

