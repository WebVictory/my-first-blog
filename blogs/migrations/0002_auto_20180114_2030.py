# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-14 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPostNew',
            fields=[
                ('blogpost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.BlogPost')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogpost',),
        ),
        migrations.RemoveField(
            model_name='blog',
            name='post',
        ),
        migrations.AddField(
            model_name='blogpostnew',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog'),
        ),
    ]
