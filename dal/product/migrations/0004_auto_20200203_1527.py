# Generated by Django 3.0.2 on 2020-02-03 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('product', '0003_remove_review_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='user_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Profile'),
        ),
    ]