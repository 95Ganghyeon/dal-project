# Generated by Django 3.0.1 on 2020-01-31 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20200121_1501'),
        ('user', '0003_remove_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='survey_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Survey'),
        ),
    ]
