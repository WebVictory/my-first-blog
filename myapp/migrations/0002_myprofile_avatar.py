# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-26 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myprofile',
            name='avatar',
            field=models.ImageField(default='uploads\\gallery\\Berlin, Germany.jpg', upload_to='uploads/'),
        ),
    ]
