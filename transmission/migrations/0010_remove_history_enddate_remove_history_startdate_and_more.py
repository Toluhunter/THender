# Generated by Django 4.1.5 on 2023-03-23 22:03

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transmission', '0009_transfer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='enddate',
        ),
        migrations.RemoveField(
            model_name='history',
            name='startdate',
        ),
        migrations.AddField(
            model_name='history',
            name='end_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transmission',
            name='filename',
            field=models.CharField(default='test', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transmission',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='history',
            name='status',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(-1)]),
        ),
    ]