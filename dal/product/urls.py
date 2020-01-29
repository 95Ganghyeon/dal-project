from django.urls import path
from product import views

urlpatterns = [
    path("<int:pk>", views.ProductDetail.as_view(), name="ProductDetail"),
    path('normalsearch/', views.NormalSearch, name='NormalSearch'),
    path('keywordsearch/', views.KeywordSearch, name='KeywordSearch'),
    path('comparesearch/', views.compareSearch, name='CompareSearch'),
]