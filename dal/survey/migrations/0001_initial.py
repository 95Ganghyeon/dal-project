# Generated by Django 3.0.3 on 2020-02-26 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
                ('volume_choice', models.PositiveSmallIntegerField(choices=[(1, '생리대'), (2, '탐폰'), (3, '생리컵')])),
                ('volume_score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('volume_extra_score', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
                ('sensitivity_score', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(7)])),
                ('disease_score', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
            ],
        ),
    ]
