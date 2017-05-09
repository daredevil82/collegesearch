# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 00:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170506_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='CIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('census_code', models.IntegerField(default=-1, help_text='Census 2000 occupation code')),
                ('census_occupation_title', models.CharField(db_index=True, default='', help_text='Census Occupation Title', max_length=100)),
                ('bls_code', models.CharField(db_index=True, default='', help_text='Bureau of Labor Code', max_length=100)),
                ('bls_occupation_title', models.CharField(db_index=True, default='', help_text='Bureau of Labor occupation title', max_length=100)),
                ('ombsoc_code', models.CharField(db_index=True, default='', help_text='OMB Standard Occupation Classification code', max_length=100)),
                ('ombsoc_occupation_title', models.CharField(db_index=True, default='', help_text='OMB Standard Occupation Classification title', max_length=100)),
                ('cip_code', models.CharField(db_index=True, default='', help_text='CIP code', max_length=100)),
                ('cip_occupation_title', models.CharField(db_index=True, default='', help_text='CIP occupation', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Completions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award_level', models.IntegerField(default=-1, help_text='Institution award level')),
                ('total_awards', models.IntegerField(default=-1, help_text='Total awards for this program')),
                ('total_awards_male', models.IntegerField(default=-1, help_text='Total awards of this program to men')),
                ('total_awards_female', models.IntegerField(default=-1, help_text='Total awards of this program to women')),
                ('cip', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cips', related_query_name='cip', to='app.CIP')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completions', related_query_name='completion', to='app.Institution')),
            ],
        ),
    ]