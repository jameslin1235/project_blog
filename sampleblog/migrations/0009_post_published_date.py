# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleblog', '0008_auto_20170129_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
