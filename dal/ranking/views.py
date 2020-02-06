from django.shortcuts import render
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from product.models import Review
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
    typeToRank = currentUser.profile.survey_fk.mtype # 현재유저의 타입을 나타내는 "OOOO"스트링 값임
    
    entireRankingBoard = RankingBoard.objects.all()
    # for record in entireRankingBoard: 
        
        
        
        
        # reviewWriterType = review.user_fk.profile.survey_fk.mtype # 리뷰작성자의 타입을 나타내는 "OOOO"스트링 값임
    

    context = {
        'currentUser': currentUser
    }
    return render(request, 'ranking.html', context=context)



