from django.db import models
from product.models import Product

# Create your models here.
class RankingBoard(models.Model):
    product_fk = models.OneToOneField(Product, on_delete=models.CASCADE)
    m_type = models.CharField(max_length=4)
    score = models.PositiveIntegerField()

    def __str__(self):
        return self.m_type + " " + self.product_fk + " " + str(self.score)