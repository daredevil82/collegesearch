# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 16:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170503_2352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_applicants', models.IntegerField(default=-1, help_text='Total number of applicants')),
                ('male_applicants', models.IntegerField(default=-1, help_text='Total number of male applicants')),
                ('female_applicants', models.IntegerField(default=-1, help_text='Total number of female applicants')),
                ('total_admissions', models.IntegerField(default=-1, help_text='Total number of admissions')),
                ('male_admissions', models.IntegerField(default=-1, help_text='Total number of male admissions')),
                ('female_admissions', models.IntegerField(default=-1, help_text='Total number of female admissions')),
                ('total_enrollment', models.IntegerField(default=-1, help_text='Total enrollment')),
                ('male_enrollment', models.IntegerField(default=-1, help_text='Male enrollment')),
                ('female_enrollment', models.IntegerField(default=-1, help_text='Female enrollment')),
                ('ft_enrollment', models.IntegerField(default=-1, help_text='Total full-time enrollment')),
                ('ft_male_enrollment', models.IntegerField(default=-1, help_text='Total male full-time enrollment')),
                ('ft_female_enrollment', models.IntegerField(default=-1, help_text='Total female full-time enrollment')),
                ('pt_enrollment', models.IntegerField(default=-1, help_text='Total part-time enrollment')),
                ('pt_male_enrollment', models.IntegerField(default=-1, help_text='Total male part-time enrollment')),
                ('pt_female_enrollment', models.IntegerField(default=-1, help_text='Total female part-time enrollment')),
                ('sat_reading_25', models.IntegerField(default=-1, help_text='SAT critical reading 25th percentile')),
                ('sat_reading_75', models.IntegerField(default=-1, help_text='SAT critical reading 75th percentile')),
                ('sat_math_25', models.IntegerField(default=-1, help_text='SAT math 25th percentile')),
                ('sat_math_75', models.IntegerField(default=-1, help_text='SAT math 75th percentile')),
                ('sat_writing_25', models.IntegerField(default=-1, help_text='SAT writing 25th percentile')),
                ('sat_writing_75', models.IntegerField(default=-1, help_text='SAT writing 75th percentile')),
                ('act_composite_25', models.IntegerField(default=-1, help_text='ACT composite 25th percentile')),
                ('act_composite_75', models.IntegerField(default=-1, help_text='ACT composite 75th percentile')),
                ('act_english_25', models.IntegerField(default=-1, help_text='ACT english 25th percentile')),
                ('act_english_75', models.IntegerField(default=-1, help_text='ACT english 75th percentile')),
                ('act_math_25', models.IntegerField(default=-1, help_text='ACT math 25th percentile')),
                ('act_math_75', models.IntegerField(default=-1, help_text='ACT math 75th percentile')),
                ('act_writing_25', models.IntegerField(default=-1, help_text='ACT writing 25th percentile')),
                ('act_writing_75', models.IntegerField(default=-1, help_text='ACT writing 75th percentile')),
            ],
        ),
        migrations.RemoveField(
            model_name='scores',
            name='institution',
        ),
        migrations.AlterField(
            model_name='institution',
            name='unitid',
            field=models.IntegerField(help_text='Institution unit ID', unique=True),
        ),
        migrations.DeleteModel(
            name='Scores',
        ),
        migrations.AddField(
            model_name='admissions',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Institution'),
        ),
    ]