from django.shortcuts import render
from product.models import Review
from ranking.models import RankingBoard

# Create your views here.
def updateRankingBoard():
    reviews = Review.objects.all()
    ranking_board = RankingBoard.objects.all()
    reviews = reviews.values('m_type').annotate(Avg('total_score'))
    # for row in ranking_board


def ranking(request):
    return render(request, 'ranking.html')