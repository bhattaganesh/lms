# Generated by Django 3.2.7 on 2021-10-08 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0003_post_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
