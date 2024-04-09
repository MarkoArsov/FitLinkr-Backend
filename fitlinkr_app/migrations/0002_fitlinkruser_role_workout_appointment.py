# Generated by Django 4.0.3 on 2024-04-09 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitlinkr_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitlinkruser',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('trainer', 'Trainer')], default='member', max_length=10),
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('strength', 'Strength Training'), ('cardio', 'Cardio'), ('yoga', 'Yoga'), ('pilates', 'Pilates'), ('crossfit', 'CrossFit'), ('other', 'Other')], default='other', max_length=10)),
                ('location', models.CharField(max_length=100)),
                ('available_spots', models.PositiveIntegerField()),
                ('rating', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('available_spots', models.PositiveIntegerField()),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitlinkr_app.workout')),
            ],
        ),
    ]
