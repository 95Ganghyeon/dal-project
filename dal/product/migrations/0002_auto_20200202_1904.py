# Generated by Django 3.0.2 on 2020-02-02 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='score',
        ),
        migrations.AddField(
            model_name='reviewsummary',
            name='total_score',
            field=models.FloatField(default=0),
        ),
    ]
