from django.urls import path
from product import views

urlpatterns = [
    path("<int:pk>", views.ProductDetail.as_view(), name="product-detail"),
    path("search/", views.search_list, name="SearchList"),
    path("keywordsearch/", views.KeywordSearch, name="KeywordSearch"),
    path("comparesearch/", views.compareSearch, name="compareSearch"),
]
