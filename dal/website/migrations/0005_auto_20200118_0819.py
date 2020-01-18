# Generated by Django 3.0.2 on 2020-01-17 23:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20200118_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='disease_score',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
