from django.shortcuts import render, get_object_or_404, resolve_url, redirect
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg, Q
from django.contrib.auth.decorators import login_required
from product.models import *
from product.forms import GetReviewResponseForm
from user.models import Profile, User
from django.http import JsonResponse
import urllib

# Create your views here.

def updateReviewSummary():
    """
    ReviewSummary 테이블을 UPDATE 하는 함수임(2~3일 주기로 실행될 것임)
    """
    entireTable = ReviewSummary.objects.all()
    for record in entireTable:
        productReviews = Review.objects.filter(product_fk__id=record.product_fk.id)
        if productReviews:
            record.total_score = productReviews.aggregate(avg=Avg('score'))['avg']
            record.absorbency_avg = productReviews.aggregate(avg=Avg('absorbency'))['avg']
            record.anti_odour_avg = productReviews.aggregate(avg=Avg('anti_odour'))['avg']
            record.comfort_avg = productReviews.aggregate(avg=Avg('comfort'))['avg']
            record.sensitivity_avg = productReviews.aggregate(avg=Avg('sensitivity'))['avg']
            record.save()
        else:
            pass # 리뷰가 아직 입력되지 않은 경우에는 None type을 aggregate해봐야  None type이 나옴. ReviewSummary의 필드값은 모두 Float type이어야 함.


def get_paginator(obj, page, obj_per_page, page_range):
    """
    한 페이지에 보일 paginator 숫자 범위 제한하는 함수임.
    이 함수는 paginator에 대한 dictionary 자료형을 반환함.
    이 dictonary를 context 변수 하나와 연결하여 넣은 뒤, 
    template에서 "변수명.page_obj", "변수명.page_range" 등등의 방식으로 사용하면 됨.
    """
    page = int(page) if page else 1

    paginator = Paginator(obj, obj_per_page)
    max_page = paginator.num_pages # 마지막 페이지
    start_page = int( (page - 1) / page_range ) * page_range
    end_page = start_page + page_range
    if end_page >= max_page:
        end_page = max_page

    return {
        'page_obj': paginator.get_page(page),
        'page_range': paginator.page_range[start_page:end_page],
        'has_prev': True if start_page > 1 else False,
        'has_next': True if end_page < max_page else False,
        'prev_page': (start_page),
        'next_page': (end_page + 1),
    }

def productDetail(request, pk):

    @login_required
    def makeReview(request, pk):
        """
        사용자가 리뷰 입력 폼에 맞게 입력하여 POST protocol로 넘어온 데이터를 바탕으로 새로운 Review Object를 만들어서 저장하는 함수임.
        """
        form = GetReviewResponseForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_fk = Product.objects.get(id=pk)            
            review.user_fk = request.user
            review.m_type = request.user.profile.survey_fk.mtype
            review.save()
    
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        makeReview(request=request, pk=pk)
        return redirect(product)
    else:
        bestReview = product.best_review_fk
        review_list = Review.objects.filter(product_fk = product)   

        form = GetReviewResponseForm()        
        context = {
            'product': product,
            'bestReview': bestReview,
            'review_list': review_list,
            'form': form,
        }
        return render(request, 'product_detail.html', context=context)


def normalSearch(request):
    
    product_list = Product.objects.all()
    query = request.GET.get('q')
    if query:
        query = query.replace(" ", "")
        product_list = product_list.annotate(rename=Func(F('name'), Value(' '), Value(''), function='REPLACE')).filter(rename__icontains=query)
        
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    context = {
        'product_list': product_list,
        'page_obj': page_obj,        
    }
    return render(request, 'normal_search.html', context=context)


def keywordSearch(request):
    
    query_string = ''
    ReviewSummary_list = ReviewSummary.objects.all()
    
    # 쿼리스트링 생성 for paginator
    if request.META['QUERY_STRING']:        
        for item in request.META['QUERY_STRING'].split('&'):
            if 'page' not in item:
                query_string += '&' + item
        print(query_string)

    if request.GET.get("keyword") == "score":
        ReviewSummary_list = ReviewSummary_list.order_by('-total_score')
    elif request.GET.get("keyword") == "absorbency":
        ReviewSummary_list = ReviewSummary_list.order_by('-absorbency_avg')
    elif request.GET.get("keyword") == "anti_odour":
        ReviewSummary_list = ReviewSummary_list.order_by('-anti_odour_avg')
    elif request.GET.get("keyword") == "comfort":
        ReviewSummary_list = ReviewSummary_list.order_by('-comfort_avg')
    elif request.GET.get("keyword") == "sensitivity":
        ReviewSummary_list = ReviewSummary_list.order_by('-sensitivity_avg')
    else:
        ReviewSummary_list = ReviewSummary_list.order_by('-total_score')
    
    page = request.GET.get('page')
    paginator = get_paginator(ReviewSummary_list, page, 1, 2)

    context = {    
        'product_list': ReviewSummary_list,
        'paginator': paginator,
        'query_string': query_string,
    }
    return render(request, "keyword_search.html", context=context)    
    

def compareSearch(request):
    
    first_page = True
    ReviewSummary_list = None
    paginator = None
    query_string = ''
    all_products = list(Product.objects.values('name').order_by('name'));
    option = None
    option_res = None # 앞단으로 보내줄 변수

    # 쿼리스트링 생성 for paginator
    if request.META['QUERY_STRING']:
        for item in request.META['QUERY_STRING'].split('&'):
            if 'page' not in item:
                query_string += '&' + item

    if 'q' in request.GET:
        first_page = False
        query = request.GET.get('q')   
        ReviewSummary_list = ReviewSummary.objects.all()

        if query not in ReviewSummary_list.values_list('product_fk__name', flat=True): # 검색 결과 없을 때
            return render(request, 'compare_search.html', {'first_page': first_page, 'searchedWord': query, 'all_products': all_products,}) 
        else: # 검색 결과 존재할 때
            criterionReviewSummary = ReviewSummary_list.get(product_fk__name=query)
            compareCondition = request.GET.get('compareConditionList').split(',')            
            if 'price' in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(product_fk__price__lt=criterionReviewSummary.product_fk.price)
            if 'nature_friendly' in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(product_fk__nature_friendly__gt=criterionReviewSummary.product_fk.nature_friendly)
            if 'absorbency' in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(absorbency_avg__gt=criterionReviewSummary.absorbency_avg)
            if 'comfort' in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(comfort_avg__gt=criterionReviewSummary.comfort_avg)
            if 'anti_odour' in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(anti_odour_avg__gt=criterionReviewSummary.anti_odour_avg)
            if 'sensitivity' in compareCondition:
                ReviewSummary_list = ReviewSummary_list.filter(sensitivity_avg__gt=criterionReviewSummary.sensitivity_avg)

            """ 
            정렬 옵션에 따른 order by
            """
            if 'option' in request.GET and request.GET.get('option') != '':
                option = request.GET.get('option')   
            else: # 쿼리스트링에 option 이 없거나, option= 인 경우 (초기화면 고려)
                option = compareCondition[0]

            option_res = option # 앞단으로 보낼 option 변수 생성 (변형 전)

            # orm 에 알맞게 변형
            if option == 'price':
                option = 'product_fk__' + option
            elif option == 'nature_friendly':
                option = '-product_fk__' + option
            else:
                option = '-' + option +'_avg'

            ReviewSummary_list = ReviewSummary_list.order_by(option)
            
            page = request.GET.get('page')
            paginator = get_paginator(ReviewSummary_list, page, 1, 2)
            
    context = {
        'first_page': first_page,
        'product_list': ReviewSummary_list,
        'paginator': paginator,
        'all_products': all_products,
        'option': option_res,
        'query_string': query_string,
    }

    return render(request, "compare_search.html", context=context)

