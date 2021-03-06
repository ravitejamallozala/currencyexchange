# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-06-29 14:35
from __future__ import unicode_literals

from django.db import migrations
import os
import settings
from django.core.management import call_command


def load_fixtures(apps, schema_editor):
    fixture1_filename = "fixtures/group.json"
    fixture1_file = os.path.join(settings.PROJECT_PATH, fixture1_filename)
    call_command(
        "loaddata", fixture1_file
    )


class Migration(migrations.Migration):
    dependencies = [
        ('exchange_backend', '0005_auto_20210626_1500'),
    ]

    operations = [
        migrations.RunPython(load_fixtures),
    ]
