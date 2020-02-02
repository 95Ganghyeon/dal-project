from django import forms
from .models import Profile

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

  def signup(self, request, user):
      user.save()
      profile = Profile()
      profile.user = user
      profile.nickname = self.cleaned_data['nickname']
      profile.birth_date = self.cleaned_data['birth_date']
      profile.save()