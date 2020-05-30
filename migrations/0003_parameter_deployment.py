# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-19 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("deployments", "0002_auto_20200418_2016"),
    ]

    operations = [
        migrations.AddField(
            model_name="parameter",
            name="deployment",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="deployments.Deployment",
                verbose_name="Deployment",
            ),
            preserve_default=False,
        ),
    ]