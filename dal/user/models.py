from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from survey.models import Survey
from datetime import datetime

class Profile(models.Model):
    user_fk = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ghost_user = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20, unique=True,)
    birth_date = models.DateField()

    m_type = models.CharField(null = True, blank=True,max_length=4)
    survey_fk = models.OneToOneField(Survey,on_delete=models.CASCADE,null = True, blank=True)

    # 유저 나이 계산함수 (리뷰에 삽입됩니다.)
    def age(self):
        age_calculate = datetime.now().year - self.birth_date.year
        return age_calculate + 1

# 찜한 생리대 
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product',on_delete=models.CASCADE,null = True, blank=True)

class Meta:
    db_table = "account_profile"
    app_label = "account"

