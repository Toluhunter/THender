# Generated by Django 4.1.5 on 2023-03-08 06:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transmission',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('file_hash', models.CharField(max_length=256)),
                ('bytes_sent', models.PositiveBigIntegerField()),
                ('total_size', models.PositiveBigIntegerField()),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieving', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sending', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Peer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ManyToManyField(related_name='peers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=80)),
                ('startdate', models.DateTimeField(auto_now_add=True)),
                ('enddate', models.DateTimeField(null=True)),
                ('status', models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(-1)])),
                ('reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recieved', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
