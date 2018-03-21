# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-24 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sentry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Person'),
        ),
    ]
