# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-18 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import re2o.mixins


class Migration(migrations.Migration):

    dependencies = [
        ("deployments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Preferences",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "compagnon_url",
                    models.URLField(
                        default="", verbose_name="URL for the compagnon website."
                    ),
                ),
            ],
            bases=(re2o.mixins.RevMixin, re2o.mixins.AclMixin, models.Model),
        ),
        migrations.DeleteModel(name="Preference",),
    ]
