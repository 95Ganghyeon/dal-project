from django.shortcuts import render
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from product.models import Review, Product
from ranking.models import RankingBoard

# Create your views here.

def updateRankingBoard():
    """
    RankingBoard 테이블을 UPDATE 하는 함수임(2~3일 주기로 실행될 것임)
    """    
    entireTable = RankingBoard.objects.all()    
    for record in entireTable:
        matchingReviews = Review.objects.filter(product_fk=record.product_fk, m_type=record.m_type)
        if matchingReview:
            record.score = matchingReviews.aggregate(avg=Avg('score')).avg
            record.save()
        else:
            pass # '리뷰가 아직 입력되지 않은 경우에는 None type을 aggregate해봐야  None type이 나옴. RankingBoard의 score필드값은 Float type이어야 함.


@login_required
def ranking(request):

    def weightCalculate(userMtype, reviewMtype):
        cnt = 0
        for char in userMtype:
            if char in reviewMtype:
                cnt += 1
        
        if cnt == 4: # 타입 스트링이 4개 전부 일치하면 가중치로 '1'을 반환
            return 1
        elif cnt == 3: # 타입 스트링이 3개만 일치하면 가중치로 '0.75'을 반환
            return 0.75
        elif cnt == 2: # 타입 스트링이 2개만 일치하면 가중치로 '0.75'을 반환
            return 0.5
        else: # 나머지 경우에는 가중치로 '0'을 반환
            return 0 


    currentUser = request.user
    currentUserType = currentUser.profile.survey_fk.mtype # 현재유저의 타입을 나타내는 "OOOO"스트링 값임
    
    """
    product_id_list = Product.objects.values_list('id', flat=True) # flat =True : 파이썬의 리스트 [] 자료구조로 필드값들을 반환
    temp_dic = {}
    for product_id in product_id_list:
        temp = 0        
        for record in RankingBoard.objects.filter(product_fk__id=product_id):            
            temp += record.score * weightCalculate(currentUserType, record.m_type)
        
        temp_dic[product_id] = temp
    
    result_dic = sorted(temp_dic.items(), key=lambda x: x[1], reverse=True)
    products = []    
    for product in result_dic:
        products += Product.objects.get(id=product.keys())
        
    # products = result_table.order_by('weightReflectedScore')        
    """
    products = Product.objects.all()
    
    
    context = {
        'currentUser': currentUser,
        'products': products,
    }
    return render(request, 'ranking.html', context=context)



