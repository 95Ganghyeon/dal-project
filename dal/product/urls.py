from django.urls import path
from product import views

urlpatterns = [
    path('', views.ProductDetail, name='ProductDetail'),  
    path('search/', views.search_list, name='SearchList'),
    path('keywordsearch/', views.KeywordSearch, name='KeywordSearch'),
    path('comparesearch/', views.compareSearch, name='compareSearch'),
]