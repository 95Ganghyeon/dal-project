# Generated by Django 3.0.3 on 2020-02-19 06:29

from django.conf import settings
import django.core.validators
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
                ('price', models.PositiveIntegerField()),
                ('count', models.IntegerField()),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('content', models.TextField()),
                ('m_type', models.CharField(max_length=4)),
                ('score', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=None, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('absorbency', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=None, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('anti_odour', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=None, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('sensitivity', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=None, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comfort', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=None, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('product_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cover_layer_string', models.TextField()),
                ('cover_layer_score', models.IntegerField(choices=[(0, '0점'), (10, '10점'), (20, '20점'), (30, '30점'), (40, '40점')], default=None, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('absorbent_layer_string', models.TextField()),
                ('absorbent_layer_score', models.IntegerField(choices=[(0, '0점'), (10, '10점'), (20, '20점'), (30, '30점'), (40, '40점')], default=None, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('etc_string', models.TextField()),
                ('etc_score', models.IntegerField(choices=[(0, '0점'), (10, '10점'), (20, '20점'), (30, '30점'), (40, '40점')], default=None, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(40)])),
                ('nature_friendly_score', models.FloatField(editable=False)),
                ('product_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
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
