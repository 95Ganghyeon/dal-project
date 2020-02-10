from django.db import models
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
    sensitivity_score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(7)])
    disease_score = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    
    def get_mtype(self):
        str = 'AHSP'
        if self.activity_score < 4: # 활동량(1~3점I,4~6점A)
            str = str.replace('A', 'I')
        if self.volume_score < 3 or (self.volume_score == 3 and self.volume_extra_score == 3): # 월경량(1~2점L,4~5점H) / 추가질문(3번L,1~2번H)
            str = str.replace('H', 'L')
        if self.sensitivity_score < 4: # 민감도(1~3점T,4~7점S)
            str = str.replace('S', 'T')
        if self.disease_score < 1: # 월경질환(0점F,1~7점P)
            str = str.replace('P', 'F')
        return str
    
    mtype = property(get_mtype)
    
    # def __str__(self):
    #     return self.mtype