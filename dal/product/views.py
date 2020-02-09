from django.shortcuts import render, get_object_or_404, resolve_url, redirect
from django.core.paginator import Paginator
from django.db.models import F, Func, Value, Avg, Q
from django.contrib.auth.decorators import login_required
from product.models import *
from product.forms import GetReviewResponseForm
from user.models import Profile, User
from django.http import JsonResponse

# Create your views here.

def updateReviewSummary():
    """
    ReviewSummary 테이블을 UPDATE 하는 함수임(2~3일 주기로 실행될 것임)
    """
    entireTable = ReviewSummary.objects.all()
    for record in entireTable:
        productReviews = Review.objects.filter(product_fk__id=record.product_fk.id)
        if productReviews:
            record.absorbency_avg = productReviews.aggregate(avg=Avg('absorbency'))['avg']
            record.anti_odour_avg = productReviews.aggregate(avg=Avg('anti_odour'))['avg']
            record.comfort_avg = productReviews.aggregate(avg=Avg('comfort'))['avg']
            record.sensitivity_avg = productReviews.aggregate(avg=Avg('sensitivity'))['avg']
            record.save()
        else:
            pass # 리뷰가 아직 입력되지 않은 경우에는 None type을 aggregate해봐야  None type이 나옴. ReviewSummary의 필드값은 모두 Float type이어야 함.

      

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
    
    def makeListOrderbyKeyword(keyword):
        """
        html radio에서 사용자가 체크한 항목에 맞는 기준으로 Product를 정렬하여, 그 데이터를 바탕으로 랜더링 해주는 함수임
        """
        product_list = []
        review_list = Review.objects.values('product_fk__id').annotate(avgOrder = Avg(keyword)).order_by('-avgOrder')
        for review in review_list:
            product_list += Product.objects.filter(id=review['product_fk__id'])            
        
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
        return render(request, "keyword_search.html", context=context)

    if request.GET.get("keyword") == "score":
        return makeListOrderbyKeyword("score")
    elif request.GET.get("keyword") == "absorbency":
        return makeListOrderbyKeyword("absorbency")
    elif request.GET.get("keyword") == "anti_odour":
        return makeListOrderbyKeyword("anti_odour")
    elif request.GET.get("keyword") == "comfort":
        return makeListOrderbyKeyword("comfort")
    elif request.GET.get("keyword") == "sensitivity":
        return makeListOrderbyKeyword("sensitivity")
    else:
        return makeListOrderbyKeyword('score')


def compareSearch(request):
    first_page = True
    ReviewSummary_list = None
    criterionReviewSummary = None
    page_obj = None
    all_products = list(Product.objects.values('name').order_by('name'));
    option = None
    option_res = None # 앞단으로 보내줄 변수

    if 'q' in request.GET:
        first_page = False
        query = request.GET.get('q')   
        ReviewSummary_list = ReviewSummary.objects.all()

        if query not in ReviewSummary_list.values_list('product_fk__name', flat=True): # 검색 결과 없을 때
            return render(request, 'compare_search.html', {'first_page': first_page, 'searchedWord': query, 'all_products': all_products,}) 
        else: # 검색 결과 존재할 떄
            criterionReviewSummary = ReviewSummary_list.get(product_fk__name=query)
            compareCondition = request.GET.get('compareConditionList')
            compareCondition = compareCondition.split(',')

            print(compareCondition[0])
            
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

            paginator = Paginator(ReviewSummary_list, 2)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

    context = {
        'first_page': first_page,
        'product_list': ReviewSummary_list,
        'page_obj': page_obj,
        'all_products': all_products,
        'option': option_res,
    }

    return render(request, "compare_search.html", context=context)

