# Generated by Django 3.2.7 on 2021-10-02 04:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='submit',
            unique_together={('assignment', 'student')},
        ),
    ]
