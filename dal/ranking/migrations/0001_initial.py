# Generated by Django 3.0.2 on 2020-02-06 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_type', models.CharField(max_length=4)),
                ('score', models.PositiveIntegerField()),
                ('product_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
    ]
