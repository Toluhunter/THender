# Generated by Django 4.1.5 on 2023-03-17 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transmission', '0004_rename_users_online_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='transmission',
            name='file_location',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transmission',
            name='file_hash',
            field=models.CharField(max_length=65),
        ),
    ]
