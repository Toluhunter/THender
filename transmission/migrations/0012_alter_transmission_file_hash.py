# Generated by Django 4.1.5 on 2023-03-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transmission', '0011_rename_filename_transmission_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transmission',
            name='file_hash',
            field=models.CharField(max_length=65),
        ),
    ]
