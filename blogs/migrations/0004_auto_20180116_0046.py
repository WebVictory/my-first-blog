# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-15 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20180115_2356'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='MyBlog',
        ),
    ]