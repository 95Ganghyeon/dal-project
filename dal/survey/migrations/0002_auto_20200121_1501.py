# Generated by Django 3.0.2 on 2020-01-21 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='sensitivy_score',
            new_name='sensitivity_score',
        ),
    ]
