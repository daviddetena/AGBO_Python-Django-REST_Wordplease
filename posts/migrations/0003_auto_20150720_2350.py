# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_auto_20150720_2212'),
        ('posts', '0002_auto_20150720_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.AddField(
            model_name='post',
            name='blog',
            field=models.OneToOneField(default=1, to='blogs.Blog'),
            preserve_default=False,
        ),
    ]
