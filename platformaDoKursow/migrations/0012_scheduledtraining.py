# Generated by Django 4.2.7 on 2023-12-12 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('platformaDoKursow', '0011_alter_quizattempt_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_duration', models.FloatField(default=30)),
                ('starting_time', models.DateTimeField()),
                ('ending_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'scheduled_trainings',
            },
        ),
    ]