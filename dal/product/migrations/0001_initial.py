# Generated by Django 3.0.1 on 2020-01-30 03:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('score', models.IntegerField()),
                ('price', models.PositiveIntegerField()),
                ('count', models.IntegerField()),
                ('category', models.CharField(max_length=30)),
                ('nature_friendly', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReviewSummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absorbency_avg', models.FloatField(default=0)),
                ('anti_odour_avg', models.FloatField(default=0)),
                ('comfort_avg', models.FloatField(default=0)),
                ('sensitivity_avg', models.FloatField(default=0)),
                ('product_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('star', models.PositiveSmallIntegerField()),
                ('absorbency', models.PositiveSmallIntegerField()),
                ('anti_odour', models.PositiveSmallIntegerField()),
                ('comfort', models.PositiveSmallIntegerField()),
                ('sensitivity', models.PositiveSmallIntegerField()),
                ('product_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RankingBoard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=4)),
                ('ranking', models.PositiveSmallIntegerField()),
                ('product_fk', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='best_review_fk',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Review'),
        ),
        migrations.AddField(
            model_name='product',
            name='hashtag_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Hashtag'),
        ),
    ]
