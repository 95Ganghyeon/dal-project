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


class ReviewSummary(models.Model):
    product_fk = models.OneToOneField(Product, on_delete=models.CASCADE)
    total_score = models.FloatField(default=0)  # Review 모델의 star 필드로 계산되는 제품 평점
    absorbency_avg = models.FloatField(default=0)
    anti_odour_avg = models.FloatField(default=0)
    comfort_avg = models.FloatField(default=0)
    sensitivity_avg = models.FloatField(default=0)

    def __str__(self):
        return self.product_fk.name + "에 대한 ReviewSummary"    

