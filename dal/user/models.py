from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from survey.models import Survey
from product.models import Product
from datetime import datetime

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user_fk = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ghost_user = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    survey_fk = models.OneToOneField(Survey,on_delete=models.CASCADE,null = True, blank=True)
    myProduct_fk = models.ManyToManyField(Product, related_name="myProduct")
    zzimProduct_fk = models.ManyToManyField(Product, related_name="zzimProduct")

    # 유저 나이 계산함수 (리뷰에 삽입됩니다.)
    def age(self):
        age_calculate = datetime.now().year - self.birth_date.year
        return age_calculate + 1

    # 내 생리대 등록은 최대 4개까지만 가능함
    # def clean(self, *args, **kwargs):
    #     if self.myProduct_fk.count() > 4:
    #         raise ValidationError("내 생리대는 최대 4개까지만 등록할 수 있습니다.")
    #     super(Profile, self).clean(*args, **kwargs)

class Meta:
    db_table = "account_profile"
    app_label = "account"

