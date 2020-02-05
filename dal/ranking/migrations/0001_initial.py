

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('m_type', models.CharField(max_length=4)),
                ('ranking', models.PositiveSmallIntegerField()),
                ('product_fk', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Product')),
            ],
        ),
    ]
