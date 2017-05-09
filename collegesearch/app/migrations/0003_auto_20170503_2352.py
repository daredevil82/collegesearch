# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 23:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170503_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuition',
            name='book_cost',
        ),
        migrations.RemoveField(
            model_name='tuition',
            name='cost_fees',
        ),
        migrations.RemoveField(
            model_name='tuition',
            name='room_board_cost',
        ),
        migrations.AlterField(
            model_name='tuition',
            name='academic_year_2014_board',
            field=models.IntegerField(default=-1, help_text='2014 academic year on-campus room and board'),
        ),
        migrations.AlterField(
            model_name='tuition',
            name='academic_year_2015_board',
            field=models.IntegerField(default=-1, help_text='2015 academic year on-campus room and board'),
        ),
    ]