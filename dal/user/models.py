from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from survey.models import Survey
from datetime import datetime


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ghost_user = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20, unique=True,)
    birth_date = models.DateField()
    
    # SEX_CHOICES= [
    #     ('MALE','M'),
    #     ('FEMALE','F'),
    # ]
    
    # sex = models.CharField(choices = SEX_CHOICES,max_length=6)
    m_type = models.CharField(null = True, blank=True,max_length=6)
    survey_id = models.OneToOneField(Survey,on_delete=models.CASCADE,null = True, blank=True)

    # 유저 나이 계산함수 (리뷰에 삽입됩니다.)
    def age(self):
        age_calculate = datetime.now().year - self.birth_date.year
        return age_calculate + 1


class Meta:
    db_table = "account_profile"
    app_label = "account"

