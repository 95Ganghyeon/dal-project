from django.urls import path
from product import views

urlpatterns = [
    path('', views.product_details, name='product_details'),  
    path('search/', views.search_list.as_view(), name='search_list'),   
] 




