# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 02:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pace', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pacechapter',
            old_name='completed_date',
            new_name='complete_date',
        ),
    ]
