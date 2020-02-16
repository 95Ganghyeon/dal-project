from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Profile
# Create your views here.

@login_required
def profile(request):
  
  try:
    profile = request.user.profile
    m_type = profile.m_type
  except:
    m_type = "검사하러 가기"
  
  try:
    n_result = request.user.cart.product_set.count()
    products = request.user.cart.product
  except:
    n_result = 0
    products = False

  context = {'m_type':m_type, 'n_result':n_result, 'products':products}
  return render(request,'user/profile.html',context=context)

def edit_profile(request):
  if request.method == 'POST':
    return HttpResponseRedirect('')
  else:
    profile = request.user.profile
    placeholder = {'nickname':profile.nickname,'email':request.user.email}
    warning = {'nickname':"변경할 닉네임 입력해주세요","email":"변경할 이메일 입력해주세요"}
    context = {'placeholder':placeholder,'warning':warning}
    return render(request,'user/profile_change.html',context=context)