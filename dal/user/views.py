from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile
from product.views import get_paginator

# Create your views here.

@login_required
def profile(request):
  
  try:
    profile = request.user.profile
    m_type = profile.survey_fk.mtype
  except:
    m_type = "M-type 없음! 검사를 실시해주세요."
  

  zzimProduct_list = profile.zzimProduct_fk.all()
  page = request.GET.get("page")
  paginator = get_paginator(zzimProduct_list, page, 1, 2)
  

  context = {
    'm_type': m_type, 
    'profile': profile,
    "paginator": paginator,
  }
  return render(request,'user/profile.html',context=context)


def edit_profile(request):
  if request.method == 'POST':
    return HttpResponseRedirect('')
  else:
    profile = request.user.profile
    placeholder = {'nickname':profile.nickname,'email':request.user.email}
    warning = {'nickname':"변경할 닉네임 입력해주세요","email":"변경할 이메일 입력해주세요"}
    context = {'placeholder':placeholder,'warning':warning}
    return render(request,'user/profile_edit.html',context=context)