<<<<<<< HEAD
# Generated by Django 3.0.3 on 2020-03-07 03:09
=======
# Generated by Django 3.0.2 on 2020-03-08 01:51
>>>>>>> 53b903da912a4b3eb49ae0d7060a75a69c74cdf0

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('survey', '0001_initial'),
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ghost_user', models.BooleanField(default=False)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('birth_date', models.DateField()),
                ('myProduct_fk', models.ManyToManyField(related_name='myProduct', to='product.Product')),
                ('survey_fk', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Survey')),
                ('user_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zzimProduct_fk', models.ManyToManyField(related_name='zzimProduct', to='product.Product')),
            ],
        ),
    ]
