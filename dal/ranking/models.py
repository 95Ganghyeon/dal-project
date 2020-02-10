from django.db import models
from product.models import Product

# Create your models here.
class RankingBoard(models.Model):
    id = models.AutoField(primary_key=True)
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
    m_type = models.CharField(max_length=4)
    score_avg = models.FloatField(default=0)

    # def __str__(self):
    #     return self.m_type + " " + self.product_fk + " " + str(self.score)