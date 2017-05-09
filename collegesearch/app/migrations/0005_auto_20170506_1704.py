# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170506_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissions',
            name='institution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
        migrations.AlterField(
            model_name='tuition',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutions', related_query_name='institution', to='app.Institution'),
        ),
    ]