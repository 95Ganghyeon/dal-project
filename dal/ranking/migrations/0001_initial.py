# Generated by Django 3.0.3 on 2020-02-27 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.FloatField(default=0)),
                ('absorbency_avg', models.FloatField(default=0)),
                ('anti_odour_avg', models.FloatField(default=0)),
                ('comfort_avg', models.FloatField(default=0)),
                ('sensitivity_avg', models.FloatField(default=0)),
                ('product_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='RankingBoard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('m_type', models.CharField(max_length=4)),
                ('score_avg', models.FloatField(default=0)),
                ('product_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
    ]
