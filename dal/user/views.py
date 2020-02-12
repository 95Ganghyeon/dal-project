from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile(request):
  m_type = "ISTP"
  n_result = 4
  context = {'m_type':m_type, 'n_result':4}
  return render(request,'profile.html',context=context)
