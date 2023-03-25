# Generated by Django 4.1.5 on 2023-03-17 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transmission', '0005_transmission_file_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transmission',
            name='file_hash',
            field=models.CharField(max_length=65, unique=True),
        ),
        migrations.AlterField(
            model_name='transmission',
            name='file_location',
            field=models.TextField(unique=True),
        ),
    ]