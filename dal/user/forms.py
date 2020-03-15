from django import forms
from .models import Profile
from survey.models import Survey

import datetime
class SignupForm(forms.Form):

  #set years range
  YEARS = [x for x in range(1940,int(datetime.datetime.now().year))]

  nickname = forms.CharField(label='nickname',
                             max_length=12,
                             widget=forms.TextInput(
                               attrs={'placeholder':'nickname',}
                             ))

  birth_date = forms.DateField(label = 'birth_date',
                                     initial = '1990-06-15',
                                     widget = forms.SelectDateWidget(years=YEARS)
  )
  def clean_nickname(self):
    nickname = self.cleaned_data['nickname']
    if Profile.objects.filter(nickname=nickname).exists():
      raise forms.ValidationError("닉네임이 이미 존재합니다")
    return nickname
  def signup(self, request, user):
    user.save()
    profile = Profile()
    profile.user_fk = user
    profile.nickname = self.clean_nickname()
    profile.birth_date = self.cleaned_data['birth_date']
    profile.save()