from django.db import models
from product.models import Product

# Create your models here.
class RankingBoard(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=4)
    product_fk = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    ranking = models.PositiveSmallIntegerField()