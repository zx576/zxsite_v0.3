# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 02:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zxsite', '0002_article_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='abstract',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='摘要'),
        ),
    ]
