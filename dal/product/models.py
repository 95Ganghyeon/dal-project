from django.db import models
from user.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True) # 등록된 시간
    updated = models.DateTimeField(auto_now=True) # 업데이트된 시간
    
    class Meta:
        abstract = True

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True) 
    best_review = models.IntegerField()
    score = models.IntegerField()
    price = models.PositiveIntegerField()
    count = models.IntegerField()
    category = models.CharField(max_length=30) # 같은 회사의 생리대라고 하더라도 [팬티라인, 소, 중, 대, ...]의 카테고리가 있음
    hashtag = models.ForeignKey('Hastag', on_delete=models.SET_NULL, null=True)
    nature_friendly = models.PositiveIntegerField()
    # ingredients = models.TextField() # 막대그래프나 선그래프로 표현될 것... # 삭제
    
    def __str__(self):
        return self.name
        
    def search_string(self):
        return self.name.replace(" ","")
        

class RankingBoard(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=4)
    product_id = models.OneToOneField('Product', on_delete=models.SET_NULL, null=True)
    ranking = models.PositiveSmallIntegerField()
    
    
class Review(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(blank=True) 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=30) # 제목
    content = models.TextField() # 설명란
    star = models.PositiveSmallIntegerField() # 별점
    absorbency = models.PositiveSmallIntegerField() # 흡수력
    anti_odour = models.PositiveSmallIntegerField() # 탈취성
    comfort = models.PositiveSmallIntegerField() # 촉감/착용감
    sensitivity = models.PositiveSmallIntegerField() # 피부친화도
    
    
class Hastag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name