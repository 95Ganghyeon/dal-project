from django.shortcuts import render
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from product.models import Review, Product
from ranking.models import RankingBoard

# Create your views here.

def updateRankingBoard():
    """
    RankingBoard 테이블을 UPDATE 하는 함수임(2~3일 주기로 실행될 것임)
    (!!!) 직접 실행시켜보니 코스트가 매우 큰거 같음. 반드시 주기적으로 실행되야 할듯함.
    """    
    entireTable = RankingBoard.objects.all()    
    for record in entireTable:
        matchingReviews = Review.objects.filter(product_fk=record.product_fk, m_type=record.m_type)
        if matchingReviews:
            record.score_avg = matchingReviews.aggregate(avg=Avg('score'))['avg']            
            record.save()
        else:
            pass # '리뷰가 아직 입력되지 않은 경우에는 None type을 aggregate해봐야  None type이 나옴. RankingBoard의 score필드값은 Float type이어야 함.


@login_required
def ranking(request):

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
        elif cnt == 2: 
            return 0.5
        else: 
            return 0

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

    updateRankingBoard()
    currentUser = request.user
    currentUserType = currentUser.profile.survey_fk.mtype # 현재유저의 타입을 나타내는 "OOOO"스트링 값임
    
    productRanking = makeUserTypeRankingBoard(currentUserType)
    sorted_productRanking = {k: v for k, v in sorted(productRanking.items(), key=lambda item: item[1])}

    products = []
    for id in sorted_productRanking:
        products += Product.objects.filter(id=id)
    
    context = {
        'currentUser': currentUser,
        'products': products,
    }
    return render(request, 'ranking.html', context=context)



