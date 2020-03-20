from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from product.models import Review, Product
from ranking.models import *

# Create your views here.
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

def updateRankingBoard():
    """
    RankingBoard 테이블을 UPDATE 하는 함수임(2~3일 주기로 실행될 것임)
    """
    entireTable = RankingBoard.objects.all()    
    for record in entireTable:
        matchingReviews = Review.objects.filter(product_fk=record.product_fk, m_type=record.m_type)
        if matchingReviews:
            record.score_avg = matchingReviews.aggregate(avg=Avg('score'))['avg']            
            record.save()
        else:
            pass # '리뷰가 아직 입력되지 않은 경우에는 None type을 aggregate해봐야  None type이 나옴. RankingBoard의 score필드값은 Float type이어야 함.

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

def calculateWeight(userMtype, reviewMtype):
    """
    유저의 타입을 기준으로 하여 랭킹보드를 보면서 '타입 스트링이 몇개나 일치하는가'를 기준으로 가중치를 결정하여 반환함.
    # 타입 스트링이 4개 전부 일치하면 가중치로 1을 반환
    # 타입 스트링이 3개만 일치하면 가중치로 0.75를 반환
    # 타입 스트링이 2개만 일치하면 가중치로 0.5를 반환
    # 나머지 경우에는 가중치로 0을 반환
    """
    cnt = 0
    for char in userMtype:
        if char in reviewMtype:
            cnt += 1
    
    if cnt == 4: 
        return 1
    elif cnt == 3: 
        return 0.75
    elif cnt ==2: 
        return 0.5
    else:
        return 0


@login_required
def mtypeRanking(request):

    def makeUserTypeRankingBoard(userType):
        """
        유저의 타입에 맞게 가중치가 계산된 '제품 당 최종점수'가 
        {product_id : 최종점수, ...} 형태의 dictionary 자료형으로 만들어져서 반환됨.        
        예를 들어, 유저의 타입이 ALTP라면 그 타입에 맞게 계산된 결과값은
        {1:40, 2:30, 3:90, 4:75, ...} 형태로 만들어져서 반환됨.
        """
        product_id_list = Product.objects.values_list('id', flat=True).order_by('id') # <QuerySet [1,2,3,4,5,...]>
        result = {}
        for key in product_id_list:
            eachType = RankingBoard.objects.filter(product_fk__id=key)
            temp_score = 0
            for row in eachType:
                temp_score += (row.score_avg * calculateWeight(userType, row.m_type))        
            
            result[key] = temp_score
        
        return result
    
    def returnRankingBoardResult(m_type):
        productRanking = makeUserTypeRankingBoard(m_type)
        sorted_productRanking = {k: v for k, v in sorted(productRanking.items(), key=lambda item: item[1])}

        products = []
        for id in sorted_productRanking:
            products += Product.objects.filter(id=id)
        
        context = {
            'm_type': m_type, # 유저 통쨰로 뷰에 넘기는건 좀..에러도나고..
            'products': products,
        }
        return context

    # 첨에 들어갔을 때(유저 첫 클릭시)
    if request.method == 'GET':
        currentUser = request.user
        try:
            currentUser.profile.survey_fk.mtype
            currentUserType = currentUser.profile.survey_fk.mtype # 현재유저의 타입을 나타내는 "OOOO"스트링 값임
        except:
            currentUserType = 'AHTP'
            #에러나서 일단 예외문 넣어줫음 수정필(mtype 검사 안한놈이 들어갔을때) @@@@@@@@@#@#!#!#!#!#!#!
        
        #검색결과 가져옴 
        context = returnRankingBoardResult(currentUserType)
        
    if request.method == 'POST':
        m_type = 'NULL'
        print(request.POST)
        try:
            m_1 = 'A' if 'toggle-1' in request.POST else 'I'
            m_2 = 'H' if 'toggle-2' in request.POST else 'L'
            m_3 = 'S' if 'toggle-3' in request.POST else 'T'
            m_4 = 'P' if 'toggle-4' in request.POST else 'F'
            m_type = m_1 + m_2 + m_3 + m_4
            print(m_type[:4])
        except:
            pass
        context = returnRankingBoardResult(m_type[:4])

    return render(request, 'ranking/mtype_ranking.html', context=context)


def keywordRanking(request):

    query_string = ''
    ReviewSummary_list = ReviewSummary.objects.all()

    # 쿼리스트링 생성 for paginator
    if request.META['QUERY_STRING']:        
        for item in request.META['QUERY_STRING'].split('&'):
            if 'page' not in item:
                query_string += '&' + item
        print(query_string)

    if request.GET.get("keyword") == "score":
        ReviewSummary_list = ReviewSummary_list.order_by('-total_score')[:10]
    elif request.GET.get("keyword") == "absorbency":
        ReviewSummary_list = ReviewSummary_list.order_by('-absorbency_avg')[:10]
    elif request.GET.get("keyword") == "anti_odour":
        ReviewSummary_list = ReviewSummary_list.order_by('-anti_odour_avg')[:10]
    elif request.GET.get("keyword") == "comfort":
        ReviewSummary_list = ReviewSummary_list.order_by('-comfort_avg')[:10]
    elif request.GET.get("keyword") == "sensitivity":
        ReviewSummary_list = ReviewSummary_list.order_by('-sensitivity_avg')[:10]
    else:
        ReviewSummary_list = ReviewSummary_list.order_by('-total_score')[:10]    

    page = request.GET.get('page')
    paginator = get_paginator(ReviewSummary_list, page, 10, 5)

    context = {    
        'product_list': ReviewSummary_list,
        'query_string': query_string,
        'paginator': paginator,
    }
    return render(request, "ranking/keyword_ranking.html", context=context)  

