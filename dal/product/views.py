from django.shortcuts import render, get_object_or_404, resolve_url, redirect
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg, Q
from django.contrib.auth.decorators import login_required
from product.models import *
from ranking.models import *
from product.forms import GetReviewResponseForm
from product.models import *
from ranking.models import ReviewSummary
from ranking.views import calculateWeight
from user.models import Profile, User
from django.http import HttpResponse, JsonResponse
import json
import urllib

# Create your views here.

# 비교함에 상품 담기
def insert_cart(request, product_id):
    cart_list = request.session.get("cart", [])

    for idx, val in enumerate(cart_list):
        if val['id'] == product_id:
            return HttpResponse("overlap")    

    data = list(Product.objects.filter(id=product_id).values("id", "name", "image"))
    cart_list.append(data[0])
    request.session["cart"] = cart_list

    # return 할때 HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json") 를 사용해도 결과는 동일합니다
    return JsonResponse(data[0], safe=False)


# 비교함에서 삭제하기 (미완성)
def delete_cart(request, product_id):
    cart_list = request.session.get("cart")

    for idx, val in enumerate(cart_list):
        if val['id'] == product_id:
            del cart_list[idx]
            break

    request.session["cart"] = cart_list

    return HttpResponse("delete success!")

def get_paginator(obj, page, obj_per_page, page_range):
    """
    한 페이지에 보일 paginator 숫자 범위 제한하는 함수임.
    이 함수는 paginator에 대한 dictionary 자료형을 반환함.
    이 dictonary를 context 변수 하나와 연결하여 넣은 뒤, 
    template에서 "변수명.page_obj", "변수명.page_range" 등등의 방식으로 사용하면 됨.
    """
    page = int(page) if page else 1

    paginator = Paginator(obj, obj_per_page)
    max_page = paginator.num_pages  # 마지막 페이지
    start_page = int((page - 1) / page_range) * page_range
    end_page = start_page + page_range
    if end_page >= max_page:
        end_page = max_page

    return {
        "page_obj": paginator.get_page(page),
        "page_range": paginator.page_range[start_page:end_page],
        "has_prev": True if start_page > 1 else False,
        "has_next": True if end_page < max_page else False,
        "prev_page": (start_page),
        "next_page": (end_page + 1),
    }


def productDetail(request, pk):
    product = get_object_or_404(Product, id=pk)

    @login_required
    def makeReview(request, pk):
        """
        사용자가 리뷰 입력 폼에 맞게 입력하여 POST protocol로 넘어온 데이터를 바탕으로 새로운 Review Object를 만들어서 저장하는 함수임.
        """
        form = GetReviewResponseForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data["score"]
            absorbency = form.cleaned_data["absorbency"]
            anti_odour = form.cleaned_data["anti_odour"]
            sensitivity = form.cleaned_data["sensitivity"]
            comfort = form.cleaned_data["comfort"]
            content = form.cleaned_data["content"]
            Review.objects.create(
                product_fk=product,
                user_fk=request.user,
                m_type=request.user.profile.survey_fk.mtype,
                score=score,
                absorbency=absorbency,
                anti_odour=anti_odour,
                sensitivity=sensitivity,
                comfort=comfort,
                content=content,
            )

    def makeTypeBasedReviewSummary(review_list, userMtype):
        type_based_review_summary = {}
        temp_score = 0
        temp_absorbency = 0
        temp_anti_odour = 0
        temp_sensitivity = 0
        temp_comfort = 0        
        
        for record in review_list:
            temp_score += record.score * calculateWeight(userMtype, record.m_type)
            temp_absorbency += record.absorbency * calculateWeight(userMtype, record.m_type)
            temp_anti_odour += record.anti_odour * calculateWeight(userMtype, record.m_type)
            temp_comfort += record.comfort * calculateWeight(userMtype, record.m_type)
            temp_sensitivity += record.sensitivity * calculateWeight(userMtype, record.m_type)
        
        type_based_review_summary['score'] = temp_score / review_list.count()
        type_based_review_summary['absorbency'] = temp_absorbency / review_list.count()
        type_based_review_summary['anti_odour'] = temp_anti_odour / review_list.count()
        type_based_review_summary['comfort'] = temp_comfort / review_list.count()
        type_based_review_summary['sensitivity'] = temp_sensitivity / review_list.count()

        return type_based_review_summary


    if request.method == "POST":
        makeReview(request=request, pk=pk)
        return redirect(product)
    else:
        best_review = product.best_review_fk
        same_type_reviews = Review.objects.filter(product_fk=product, m_type=request.user.profile.survey_fk.mtype)
        other_type_reviews = Review.objects.filter(product_fk=product).exclude(m_type=request.user.profile.survey_fk.mtype)
        
        review_list = same_type_reviews | other_type_reviews

        type_based_review_summary = makeTypeBasedReviewSummary(review_list, request.user.profile.survey_fk.mtype)

        print(type_based_review_summary)

        page = request.GET.get("page")
        paginator = get_paginator(review_list, page, 5, 3)

        form = GetReviewResponseForm()
        context = {
            "product": product,
            "type_based_review_summary": type_based_review_summary,
            "best_review": best_review,
            "review_list": review_list,
            "paginator": paginator,
            "form": form,
        }
        return render(request, "product/product_detail.html", context=context)


def normalSearch(request):

    first_page = True
    ReviewSummary_list = None
    paginator = None
    query_string = ""
    all_products = list(Product.objects.values("name").order_by("name"))
    # option = None
    # option_res = None # 앞단으로 보내줄 변수

    # 쿼리스트링 생성 for paginator
    if request.META["QUERY_STRING"]:
        for item in request.META["QUERY_STRING"].split("&"):
            if "page" not in item:
                query_string += "&" + item

    if "q" in request.GET:
        first_page = False
        query = request.GET.get("q")
        query = query.replace(" ", "")
        ReviewSummary_list = ReviewSummary.objects.all()
        ReviewSummary_list = ReviewSummary_list.annotate(
            rename=Func(
                F("product_fk__name"), Value(" "), Value(""), function="REPLACE"
            )
        ).filter(rename__icontains=query)

        ###
        # """
        # 정렬 옵션에 따른 order by
        # """
        # if 'option' in request.GET and request.GET.get('option') != '':
        #     option = request.GET.get('option')
        # else: # 쿼리스트링에 option 이 없거나, option= 인 경우 (초기화면 고려)
        #     option = compareCondition[0]

        # option_res = option # 앞단으로 보낼 option 변수 생성 (변형 전)

        # # orm 에 알맞게 변형
        # if option == 'price':
        #     option = 'product_fk__' + option
        # elif option == 'nature_friendly':
        #     option = '-product_fk__' + option
        # else:
        #     option = '-' + option +'_avg'

        # ReviewSummary_list = ReviewSummary_list.order_by(option)
        ###

        page = request.GET.get("page")
        paginator = get_paginator(ReviewSummary_list, page, 1, 2)

    context = {
        "first_page": first_page,
        "product_list": ReviewSummary_list,
        "paginator": paginator,
        "all_products": all_products,
        # 'option': option_res,
        "query_string": query_string,
    }
    return render(request, "product/normal_search.html", context=context)


def compareSearch(request):

    first_page = True
    ReviewSummary_list = None
    paginator = None
    query_string = ""
    all_products = list(Product.objects.values("name").order_by("name"))
    option = None
    option_res = None  # 앞단으로 보내줄 변수

    # 쿼리스트링 생성 for paginator
    if request.META["QUERY_STRING"]:
        for item in request.META["QUERY_STRING"].split("&"):
            if "page" not in item:
                query_string += "&" + item

    if "q" in request.GET:
        first_page = False
        query = request.GET.get("q")
        ReviewSummary_list = ReviewSummary.objects.all()

        if query not in ReviewSummary_list.values_list(
            "product_fk__name", flat=True
        ):  # 검색 결과 없을 때
            return render(
                request,
                "product/compare_search.html",
                {
                    "first_page": first_page,
                    "searchedWord": query,
                    "all_products": all_products,
                },
            )
        else:  # 검색 결과 존재할 때
            criterionReviewSummary = ReviewSummary_list.get(product_fk__name=query)
            compareCondition = request.GET.get("compareConditionList").split(",")
            if "price" in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(
                    product_fk__price__lt=criterionReviewSummary.product_fk.price
                )
            if "nature_friendly" in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(
                    product_fk__productingredient__nature_friendly_score__gt=criterionReviewSummary.product_fk.productingredient.nature_friendly_score
                )
            if "absorbency" in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(
                    absorbency_avg__gt=criterionReviewSummary.absorbency_avg
                )
            if "comfort" in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(
                    comfort_avg__gt=criterionReviewSummary.comfort_avg
                )
            if "anti_odour" in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(
                    anti_odour_avg__gt=criterionReviewSummary.anti_odour_avg
                )
            if "sensitivity" in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(
                    sensitivity_avg__gt=criterionReviewSummary.sensitivity_avg
                )

            """ 
            정렬 옵션에 따른 order by
            """
            if "option" in request.GET and request.GET.get("option") != "":
                option = request.GET.get("option")
            else:  # 쿼리스트링에 option 이 없거나, option= 인 경우 (초기화면 고려)
                option = compareCondition[0]

            option_res = option  # 앞단으로 보낼 option 변수 생성 (변형 전)

            # orm 에 알맞게 변형
            if option == "price":
                option = "product_fk__" + option
            elif option == "nature_friendly":
                option = "-product_fk__productingredient__" + option + "_score"
            else:
                option = "-" + option + "_avg"

            # ReviewSummary_list = ReviewSummary_list.order_by(option)

            page = request.GET.get("page")
            paginator = get_paginator(ReviewSummary_list, page, 1, 2)

    context = {
        "first_page": first_page,
        "product_list": ReviewSummary_list,
        "paginator": paginator,
        "all_products": all_products,
        "option": option_res,
        "query_string": query_string,
    }

    return render(request, "product/compare_search.html", context=context)

