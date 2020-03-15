from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Window, F, Q, Subquery
from django.db.models.functions import DenseRank
from .models import Profile
from product.models import Product
from ranking.models import ReviewSummary
from product.views import get_paginator

from allauth.account.views import *
from allauth.account.forms import *

# Create your views here.


def delete_myProduct(request, product_id):
    myProduct = get_object_or_404(Product, id=product_id)
    profile = Profile.objects.get(user_fk__id=request.user.id)
    profile.myProduct_fk.remove(myProduct)

    return HttpResponseRedirect(reverse("profile"))


@login_required
def profile(request):

    profile = request.user.profile

    try:
        m_type = profile.survey_fk.mtype
    except:
        m_type = "M-type 없음! 검사를 실시해주세요."

    # 사용자가 찜한 제품들의 id(pk)값을 리스트 형태로 받아옴
    zzimProduct_list = list(profile.zzimProduct_fk.all().values_list("id", flat=True))

    # ReviewSummary 테이블을 total_score 순으로 내림차순 정렬한뒤, annotate를 통해 순위를 나타내는 rank 주석을 달아줌
    ReviewSummary_list = ReviewSummary.objects.all().annotate(
        rank=Window(expression=DenseRank(), order_by=F("total_score").desc())
    )

    # ReviewSummary 테이블을 돌면서 사용자가 찜한 제품들을 골라서 최종 리스트(result_zzimProduct_list)에 담음
    result_zzimProduct_list = []

    for rs in ReviewSummary_list:
        if rs.product_fk.id in zzimProduct_list:
            result_zzimProduct_list.append(rs)

    print(result_zzimProduct_list)
    page = request.GET.get("page")
    paginator = get_paginator(result_zzimProduct_list, page, 6, 5)

    context = {
        "m_type": m_type,
        "profile": profile,
        "paginator": paginator,
    }

    return render(request, "user/profile.html", context=context)


def edit_profile(request):
    if request.method == "POST":
        return HttpResponseRedirect("")
    else:
        profile = request.user.profile
        placeholder = {"nickname": profile.nickname, "email": request.user.email}
        warning = {"nickname": "변경할 닉네임 입력해주세요", "email": "변경할 이메일 입력해주세요"}
        context = {"profile": profile, "placeholder": placeholder, "warning": warning}
        return render(request, "user/profile_edit.html", context=context)


# class CustomPasswordChangeView(PasswordChangeView):
#   template_name = 'user/profile.html'
#   success_url = reverse_lazy('edit_profile')

# class CustomPasswordChangeForm(PasswordChangeForm):

#   def save(self):
#     super(CustomPasswordChangeForm, self).save()

