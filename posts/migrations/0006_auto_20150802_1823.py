# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import posts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20150725_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(validators=[posts.validators.badwords_detector]),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='summary',
            field=models.CharField(max_length=200, validators=[posts.validators.badwords_detector]),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, validators=[posts.validators.badwords_detector]),
        ),
    ]
