from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .models import Profile
# Create your views here.

@login_required
def profile(request):
  print(request.user.id)
  print()
  # n_result = profile.cart.product_set.count()
  context = {'m_type':'ISTP', 'n_result':4}
  return render(request,'profile.html',context=context)
