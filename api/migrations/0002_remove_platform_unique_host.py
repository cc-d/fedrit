# Generated by Django 4.1.5 on 2023-05-20 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='platform',
            name='unique_host',
        ),
    ]
