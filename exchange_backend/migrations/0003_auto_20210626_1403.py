# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-06-26 14:03
from __future__ import unicode_literals

import os

from django.db import migrations
import os
import settings
from django.core.management import call_command


def load_fixtures(apps, schema_editor):
    fixture1_filename = "fixtures/currency.json"
    fixture1_file = os.path.join(settings.PROJECT_PATH, fixture1_filename)
    call_command(
        "loaddata", fixture1_file
    )

class Migration(migrations.Migration):
    dependencies = [
        ('exchange_backend', '0002_auto_20210626_0653'),
    ]

    operations = [
        migrations.RunPython(load_fixtures),
    ]
