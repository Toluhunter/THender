# Generated by Django 4.1.5 on 2023-03-15 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transmission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transmission',
            name='bytes_sent',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
