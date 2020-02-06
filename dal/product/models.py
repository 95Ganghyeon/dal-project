from django.db import models
from django.urls import reverse
from user.models import Profile, User
# from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)  # 등록된 시간
    updated = models.DateTimeField(auto_now=True)  # 업데이트된 시간

    class Meta:
        abstract = True


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    best_review_fk = models.OneToOneField("Review", on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField()
    count = models.IntegerField()
    category = models.CharField(max_length=30) # 같은 회사의 생리대라고 하더라도 [팬티라인, 소, 중, 대, ...]의 카테고리가 있음
    hashtag_fk = models.ForeignKey('Hashtag', on_delete=models.SET_NULL, null=True)
    nature_friendly = models.PositiveIntegerField()
    # ingredients = models.TextField() # 막대그래프나 선그래프로 표현될 것... # 삭제

    def __str__(self):
        return self.name

    def search_string(self):
        return self.name.replace(" ", "")

    def get_absolute_url(self):
        return reverse("ProductDetail", args=[str(self.id)])


class Review(TimeStampedModel):
    
    # form.py 에서 1~5까지 radio 선택지를 주기 위해서 필요함
    RANGE_ONE_TO_FIVE = (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
    )
    
    id = models.AutoField(primary_key=True)
    image = models.ImageField(blank=True) 
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE)
    product_fk = models.ForeignKey('Product', on_delete=models.CASCADE)
    content = models.TextField() # 설명란
    m_type = models.CharField(max_length=4)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None
    ) # 별점
    absorbency = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None
    ) # 흡수력
    anti_odour = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None
    ) # 탈취성
    sensitivity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None
    ) # 피부친화도
    comfort = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RANGE_ONE_TO_FIVE,
        default=None
    ) # 촉감/착용감

    
    def __str__(self):
        return self.user_fk.username + "의 리뷰"

    def star_Str(self):
        if self.star == 1:
            return "최악"
        elif self.star == 2:
            return "별로"
        elif self.star == 3:
            return "나름"
        elif self.star == 4:
            return "오오"
        elif self.star == 5:
            return "대박"
        
    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={"pk": self.id})
    
    
    
class Hashtag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ReviewSummary(models.Model):
    product_fk = models.OneToOneField('Product', on_delete=models.CASCADE)
    total_score = models.FloatField(default=0) # Review 모델의 star 필드로 계산되는 제품 평점
    absorbency_avg = models.FloatField(default=0)
    anti_odour_avg = models.FloatField(default=0)
    comfort_avg = models.FloatField(default=0)
    sensitivity_avg = models.FloatField(default=0)

    def __str__(self):
        return self.product_fk.name + "에 대한 ReviewSummary"
