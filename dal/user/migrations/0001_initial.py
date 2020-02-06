# Generated by Django 3.0.2 on 2020-02-06 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('survey', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ghost_user', models.BooleanField(default=False)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('birth_date', models.DateField()),
                ('m_type', models.CharField(blank=True, max_length=4, null=True)),
                ('survey_fk', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Survey')),
                ('user_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
