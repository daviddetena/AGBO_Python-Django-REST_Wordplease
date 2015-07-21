# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
