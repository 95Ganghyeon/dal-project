from django.db import models
from django.contrib.auth.models import User
from survey.models import Survey

class User_Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ghost_user = models.BooleanField(default=False)
    nickname = models.CharField(max_length=20, unique = True, )
    birth_date = models.DateField()
    
    SEX_CHOICES= [
        ('MALE','M'),
        ('FEMALE','F'),
    ]
    
    sex = models.CharField(choices = SEX_CHOICES,max_length=6)
    m_type = models.CharField(null = True, blank=True,max_length=6)
    survey_id = models.OneToOneField(Survey,on_delete=models.CASCADE)

    

    



