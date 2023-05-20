# Generated by Django 4.1.5 on 2023-05-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_platform_unique_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='id',
            new_name='uuid',
        ),
        migrations.AddConstraint(
            model_name='platform',
            constraint=models.UniqueConstraint(condition=models.Q(('is_host', True)), fields=('is_host',), name='unique_host'),
        ),
    ]
