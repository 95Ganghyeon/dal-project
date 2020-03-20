from django.urls import path
from ranking import views

urlpatterns = [
    path("mtype/", views.mtypeRanking, name="MtypeRanking"),
    path("keyword/", views.keywordRanking, name="KeywordRanking"),
]
