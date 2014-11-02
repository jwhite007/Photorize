# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photorizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='owner',
            field=models.ForeignKey(related_query_name=b'tag', related_name=b'tags', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
