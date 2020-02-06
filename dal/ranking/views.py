from django.shortcuts import render
from product.models import Review
from ranking.models import RankingBoard

# Create your views here.
def updateRankingBoard():
    reviews = Review.objects.all()
    ranking_board = RankingBoard.objects.all()
    reviews = reviews.values('m_type', 'product_fk').annotate(Avg('score'))
    for row in ranking_board:
        row.score = reviews.get(m_type=row.m_type, product_fk=row.product_fk).score__avg
        row.save()

def ranking(request):
    return render(request, 'ranking.html')