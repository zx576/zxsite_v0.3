# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zxsite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='zxsite.Tag', verbose_name='标签'),
        ),
    ]
