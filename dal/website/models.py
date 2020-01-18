from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Survey(models.Model):
    activity_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    
    VOLUME_CHOICE = (
        (1, '생리대'),
        (2, '탐폰'),
        (3, '생리컵'),
    )
    
    volume_choice = models.PositiveSmallIntegerField(choices=VOLUME_CHOICE)
    volume_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    volume_extra_score = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)]
    )
    sensitivy_score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(7)])
    disease_score = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    
    def type(self):
        str = 'AHSP'
        if self.activity_score < 4: # 활동량(1~3점I,4~6점A)
            str = str.replace('A', 'I')
        if self.volume_score < 3 or (self.volume_score == 3 and self.volume_extra_score == 3): # 월경량(1~2점L,4~5점H) / 추가질문(3번L,1~2번H)
            str = str.replace('H', 'L')
        if self.sensitivy_score < 4: # 민감도(1~3점T,4~7점S)
            str = str.replace('S', 'T')
        if self.disease_score < 1: # 월경질환(0점F,1~7점P)
            str = str.replace('P', 'F')
        return str
    
    def __str__(self):
        return self.type()
        

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(blank=True) 
    # best_review = models.OneToOneField('Review', on_delete=models.CASCADE)
    # review = models.ForeignKey('Review', on_delete=models.CASCADE, null=True)
    score = models.IntegerField() 
    price = models.PositiveIntegerField()
    count = models.IntegerField() 
    category = models.CharField(max_length = 30) # 같은 회사의 생리대라고 하더라도 [팬티라인, 소, 중, 대, ...]의 카테고리가 있음
    ingredients = models.TextField() 
    hashtag = models.ForeignKey('Hastag', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name
    
    
class Hastag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
        

class Ghost_user:
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
class Review:
    id = models.AutoField(primary_key=True)
    image = models.ImageField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    product_id = models.OneToOneField('Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    star = models.PositiveSmallIntegerField()
    absorbency = models.PositiveSmallIntegerField()
    anti_odour = models.PositiveSmallIntegerField()
    sensitivity = models.PositiveSmallIntegerField()
    comfort = models.PositiveSmallIntegerField()


class RankingBoard:
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=4)
    # product_id = models.OneToOneField('Product', on_delete=models.SET_NULL)
    ranking = models.PositiveSmallIntegerField()
    